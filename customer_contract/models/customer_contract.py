from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class CustomerContract(models.Model):
    _name = 'customer.contract'
    _description = 'Clients contracts'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Code', default=lambda self: self.env['ir.sequence'].next_by_code('customer.contract'), readonly=True)
    start_date = fields.Date(string='Start of contract', required=True)
    end_date = fields.Date(string='End of contract', required=True)

    partner_id = fields.Many2one('res.partner', string='Tutor', required=True)

    state = fields.Selection(selection=[
        ('in_process', 'In process'),
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('finalized','Finalized')
    ], string='Contract state', default='in_process')

    
    total_payment_amount = fields.Float(string='Total Debt', required=True)


    """
    Invoice related to contract payment
    """
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, required=False)

    """
    supplements = fields.Many2one()
    child_id = field.Many2one()
    """

    def unlink(self):
        for record in self:
            if record.invoice_id and record.invoice_id.state == 'posted':
                raise ValidationError("You cannot delete this contract because the invoice is already approved.")
            elif record.invoice_id:
                record.invoice_id.unlink() 
        return super(CustomerContract, self).unlink()

    def write(self, vals):
        res = super(CustomerContract, self).write(vals)
        if 'state' in vals and vals['state'] in ['expired', 'finalized']:
                income_account = self.env['account.account'].search([('account_type', '=', 'income')], limit=1)
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': res.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_payment_term_id': False,  
                    'invoice_line_ids': [(0, 0, {
                        'name': f'Contract Payment - {res.name}',
                        'quantity': 1,
                        'price_unit': res.total_payment_amount,
                        'account_id': income_account.id if income_account else False
                    })]
                }
                invoice = self.env['account.move'].create(invoice_vals)
                res.invoice_id = invoice.id
        return res

    
    def update_customer_tatus(self):
        today = date.today()
        contracts = self.search([('state', '=', 'valid')])
        for contract in contracts:
            if contract.end_date and contract.end_date < today:
                contract.state = 'expired'
                
                self.send_expiration_email(contract)

    
    def send_expiration_email(self, contract):
        template = self.env.ref('contract_invoice_management.email_template_contract_expiration')
        if template:
            email_values = {
                'email_to': contract.partner_id.email,  
                #'email_cc': coordinator_email,  
                'partner_ids': [(6, 0, [contract.partner_id.id])],
            }
            template.send_mail(contract.id, email_values=email_values)
        
    
                
    def action_renew_contract(self):
        for contract in self:
            if contract.state != 'expired':
                raise ValidationError("Only expired contracts can be renewed.")
            
            new_start_date = fields.Date.today()
            new_end_date = new_start_date + relativedelta(months=6)
                
            new_contract = contract.copy(default={
                'start_date': new_start_date,
                'end_date': new_end_date,
                'state': 'valid',
                'invoice_id': False 
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'customer.contract',
                'view_mode': 'form',
                'res_id': new_contract.id,
                'target': 'current',
            }
    def action_valid_contract(self):
        for contract in self:
            if contract.state != 'in_process':
                raise ValidationError("Only contracts in process can be validated.")

            contract.state = 'valid'






