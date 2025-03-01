from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class LoanService(models.Model):
    _name = 'loan.service'
    _description = 'Loan Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Code', default=lambda self: self.env['ir.sequence'].next_by_code('loan.service'),
                       readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True,
                                 domain="[('loan_applicant', '=', True)]")
    id_number = fields.Char(string='Id Number', related='partner_id.id_number', readonly=True)
    date_of_application = fields.Date(string='Date of Application', required=True)
    payment_date = fields.Date(string='Payment Date', required=True)
    loan_amount = fields.Float(string='Loan Amount')
    daily_interest_rate = fields.Float(string='Daily Interest Rate')
    interest_amount = fields.Float(string='Interest Amount', compute='_compute_interest_amount', store=True)
    total_debt = fields.Float(string='Total Debt', compute='_compute_total_debt', store=True)
    state = fields.Selection(selection=[
        ('on_time', 'On Time'),
        ('delayed', 'Delayed'),
        ('paid', 'Paid'),
    ], string='State', default='on_time')

    #Campos añadidos:
    '''
    invoice_id: relación del prestamo con la factura.
    paid_amount: calculo del dinero por pagar de acuredo con los pagos parciales realizados a la factura.
    progress: calculos del progreso en función de los pagos. 
    '''
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    paid_amount = fields.Float(string='Paid Amount', compute='_compute_paid_amount', store=True)

    progress = fields.Float(string='Payment Progress', compute='_compute_progress', store=False)


    @api.depends('paid_amount', 'total_debt')
    def _compute_progress(self):
        for record in self:
            if record.total_debt > 0:
                record.progress = (record.paid_amount / record.total_debt) * 100
            else:
                record.progress = 0.0

    @api.depends('invoice_id.amount_residual', 'invoice_id.amount_total')
    def _compute_paid_amount(self):
        for record in self:
            if record.invoice_id:
                record.paid_amount = record.invoice_id.amount_total - record.invoice_id.amount_residual
            else:
                record.paid_amount = 0.0

    def unlink(self):
        #Validación para evitar que una véz aprobada la factura no permina eliminar el prestamo
        for record in self:
            if record.invoice_id and record.invoice_id.state == 'posted':
                raise ValidationError("You cannot delete this loan because the invoice is already approved.")
            elif record.invoice_id:
                record.invoice_id.unlink() 
        return super(LoanService, self).unlink()

    @api.depends('loan_amount', 'daily_interest_rate', 'payment_date', 'date_of_application')
    def _compute_interest_amount(self):
        for record in self:
            if record.date_of_application and record.payment_date:
                days = (record.payment_date - record.date_of_application).days
                record.interest_amount = record.loan_amount * record.daily_interest_rate * days

    @api.depends('loan_amount', 'interest_amount')
    def _compute_total_debt(self):
        for record in self:
            record.total_debt = record.loan_amount + record.interest_amount

    def update_loan_status(self):
        today = date.today()
        loans = self.search([('state', '=', 'on_time')])
        for loan in loans:
            if loan.payment_date and loan.payment_date < today:
                loan.state = 'delayed'
    
    @api.depends('invoice_id.payment_state')
    def _update_state_from_invoice(self):
        
        for record in self:
            if record.invoice_id and record.invoice_id.payment_state == 'paid':
                record.state = 'paid'

    @api.model
    def create(self, vals):
        loan = super(LoanService, self).create(vals)

        income_account = self.env['account.account'].search([('account_type', '=', 'income')], limit=1)
        
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': loan.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_payment_term_id': False,  
            'invoice_line_ids': [(0, 0, {
                'name': f'Loan Payment - {loan.name}',
                'quantity': 1,
                'price_unit': loan.total_debt,
                'account_id': income_account.id if income_account else False
            })]
        }
        invoice = self.env['account.move'].create(invoice_vals)

        loan.invoice_id = invoice.id

        user = self.env['res.users'].search([('partner_id', '=', loan.partner_id.id)], limit=1)
        
        if loan.payment_date and user:
            reminder_date = fields.Date.subtract(loan.payment_date, days=3)

            loan.activity_schedule(
                activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                summary="Loan Payment Reminder",
                note=f"Your payment is due on {loan.payment_date}.",
                user_id=user.id,  
                date_deadline=reminder_date
            )

        return loan
    