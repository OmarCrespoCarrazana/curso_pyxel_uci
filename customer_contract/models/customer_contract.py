from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from calendar import monthrange

class CustomerContract(models.Model):
    _name = 'customer.contract'
    _description = 'Clients contracts'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Code', default=lambda self: self.env['ir.sequence'].next_by_code('customer.contract'), readonly=True )
    start_date = fields.Date(string='Start of contract', required=True, readonly=True, default=fields.Date.today)
    end_date = fields.Date(string='End of contract', required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Tutor', required=True)
    state = fields.Selection(selection=[
        ('valid', 'Valid'),
        ('expired', 'Expired'),
    ], string='Contract state', default='valid')
    invoice_id = fields.Many2many('account.move', string='Invoice', readonly=True, required=False)
    
    payment_day = fields.Integer(string="Day to issue the invoice.", required=True)
    
    @api.constrains("payment_day")
    def _check_payment_day_range(self):
        for record in self:
            if record.payment_day < 1 or record.payment_day > 24:
                raise ValidationError("The number of hours must be between 1 and 24.")

    @api.model
    def create(self, vals):
        if "start_date" not in vals:
            vals["start_date"] = fields.Date.today()
        if "end_date" not in vals:
            vals["end_date"] = vals["start_date"] + relativedelta(months=6)
        contract = super(CustomerContract, self).create(vals)  
            
        return contract
         
    
    
    def update_customer_tatus(self):
        today = date.today()
        contracts = self.search([('state', '=', 'valid')])
        for contract in contracts:
            if contract.end_date and contract.end_date < today:
                contract.state = 'expired'
                
                #self.send_expiration_email(contract)
                
        
        contracts_to_invoice = self.search([
            ('payment_day', '=', today.day)
        ])
        for contract in contracts_to_invoice:
            end_date_last_day = date(contract.end_date.year, contract.end_date.month, monthrange(contract.end_date.year, contract.end_date.month)[1]) + relativedelta(months=1)
            if  today <= end_date_last_day:
                self.generate_invoice_if_due(self, contract)


    def generate_invoice_if_due(self, contract):
        """
        incluir los insumos y cosos por mora 
        """
        income_account = self.env["account.account"].search([("account_type", "=", "income")], limit=1)
        invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": contract.partner_id.id,
            "invoice_date": fields.Date.today(),
            "invoice_payment_term_id": False,
            "invoice_line_ids": [(0, 0, {
                "name": f"Contract Payment - {contract.name}",
                "quantity": 1,
                "price_unit": 500,
                "account_id": income_account.id if income_account else False,
            })],
        }
        invoice = self.env["account.move"].create(invoice_vals)
        contract.invoice_id = [(4, invoice.id)]

    def send_expiration_email(self, contract):
        template = self.env.ref('customer_contract.email_template_contract_expiration')
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






