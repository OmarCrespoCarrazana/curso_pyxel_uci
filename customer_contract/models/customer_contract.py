from odoo import models, fields, api
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from calendar import monthrange

class CustomerContract(models.Model):
    _name = 'customer.contract'
    _description = 'Clients contracts'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Code',  copy=False, readonly=False, store=True )
    start_date = fields.Date(string='Start of contract', required=True, readonly=True, default=fields.Date.today)
    end_date = fields.Date(string='End of contract', required=True, readonly=True)
    
    lead_id = fields.Many2one('crm.lead', string="Lead", required=True)
    partner_id = fields.Many2one('res.partner', string='Tutor', related='lead_id.partner_id', readonly=True)
    child_id = fields.Many2one('childcare.child', string="Child", related='lead_id.child_id', readonly=True)
    
    user_id = fields.Many2one(string="Email", related='lead_id.user_id', readonly=True)
    
    
    state = fields.Selection(selection=[
        ('valid', 'Valid'),
        ('expired', 'Expired'),
    ], string='Contract state', default='valid')
    
    invoice_id = fields.Many2many('account.move', string='Invoice', readonly=True, required=False)
    
    payment_day = fields.Integer(string="Day to issue the invoice.", required=True, default=1)
    
    hide_renew_button = fields.Boolean(compute="_compute_hide_renew_button")

    @api.depends("child_id.age")
    def _compute_hide_renew_button(self):
        for contract in self:
            if contract.child_id and contract.child_id.age:
                age = int(contract.child_id.age.split(" ")[0])  
                contract.hide_renew_button = age >= 5
            else:
                contract.hide_renew_button = False
    
    
    @api.constrains("payment_day")
    def _check_payment_day_range(self):
        for record in self:
            if record.payment_day < 1 or record.payment_day > 24:
                raise ValidationError("The number of hours must be between 1 and 24.")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.code_generation(self.partner_id.vat)
            
    def code_generation(self, vat=None):
        nit = vat or "000000"  
        sequence = self.env['ir.sequence'].next_by_code('customer.contract') or '000'
        year = datetime.today().year
        return f'C-{nit}-{sequence}-{year}'

    @api.model
    def create(self, vals):
        if "start_date" not in vals:
            vals["start_date"] = fields.Date.today()
        if "end_date" not in vals:
            vals["end_date"] = vals["start_date"] + relativedelta(months=6)
        
        if not vals.get('name'):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            vals['name'] = self.code_generation(partner.vat)
        contract = super(CustomerContract, self).create(vals)  
        self.send_expiration_email(contract)
        return contract
         
    
    
    def update_customer_tatus(self):
        today = date.today()
        contracts = self.search([('state', '=', 'valid')])
        for contract in contracts:
            if contract.end_date and contract.end_date < today:
                contract.state = 'expired'
                if contract.hide_renew_button: 
                    self.send_expiration_email(contract)
                
        
        contracts_to_invoice = self.search([
            ('payment_day', '=', today.day)
        ])
        for contract in contracts_to_invoice:
            end_date_last_day = date(contract.end_date.year, contract.end_date.month, monthrange(contract.end_date.year, contract.end_date.month)[1]) + relativedelta(months=1)
            if  today <= end_date_last_day:
                self.generate_invoice_if_due(contract)


    def generate_invoice_if_due(self, contract):
        #Buscar si tiene seguro para el descuento de los insumos
        insurance = self.env["insurance"].search([("child_id", "=", contract.child_id.id)])
        if insurance:
            pay = insurance.total_amount
            print(pay)
            #Aqui devo contar los insumos para saber 
            #si los cubre el seguro y si no pues cobrarlos.
        
        #Calculo de las horas extra del niño en la guardería
        attendance_records = self.env["childcare.attendance"].search([("child_id", "=", contract.child_id.id)])
        total_extra_hours = sum(attendance.extra_hours for attendance in attendance_records)
        mora_amount = total_extra_hours * 50
        
        income_account = self.env["account.account"].search([("account_type", "=", "income")], limit=1)
        
        #Pago base del contrato
        invoice_lines = [
        (0, 0, {
            "name": f"Pago del contrato - {contract.name}",
            "quantity": 1,
            "price_unit": 500,
            "account_id": income_account.id if income_account else False,
        })
        ]
        #Incluir a la factura el pago por mora en caso de tener
        if mora_amount > 0:
            invoice_lines.append(
                (0, 0, {
                    "name": "Pago por concepto de mora",
                    "quantity": total_extra_hours,
                    "price_unit": mora_amount,
                    "account_id": income_account.id if income_account else False,
                })
            )
        
        invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": contract.partner_id.id,
            "invoice_date": fields.Date.today(),
            "invoice_payment_term_id": False,
            "invoice_line_ids": invoice_lines,
        }
        invoice = self.env["account.move"].create(invoice_vals)
        contract.invoice_id = [(4, invoice.id)]



    def send_expiration_email(self, contract):
        template = self.env.ref('customer_contract.email_template_contract_expiration')
        if template:
            template.send_mail(contract.id, force_send=True)
        
    
                
    def action_renew_contract(self):
        for contract in self:
            if contract.state != 'valid':
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






