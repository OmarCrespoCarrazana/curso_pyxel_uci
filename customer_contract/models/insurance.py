from odoo import models, fields, api
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from calendar import monthrange

class Insurance(models.Model):
    _name = 'insurance'
    _description = 'Health insurance'
    
    partner_id = fields.Many2one('res.partner', string="Cliente")
    child_id = fields.Many2one('childcare.child', string="Niño")
    
    amount = fields.Float(string="Monto a depocitar", )
    
    total_amount = fields.Float(string="Monto a cubrir", compute="_compute_total_amount")
    
    state = fields.Selection(selection=[
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ], string='Estado del seguro', default='active')
    
    
    @api.depends('amount')
    def _compute_total_amount(self):
        for record in self:
            if record.amount:
                record.total_amount = record.amount * 0.05 * record.amount
            else:
                record.total_amount = 0.0
    
    def add_new_invoice(self):
        insurances = self.search([('state', '=', 'active')])
        for insurance in insurances:
            income_account = self.env["account.account"].search([("account_type", "=", "income")], limit=1)
            invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": insurance.partner_id.id,
            "invoice_date": fields.Date.today(),
            "invoice_payment_term_id": False,
            "invoice_line_ids": [
                    (0, 0, {
                        "name": f"Pago del seguro",
                        "quantity": 1,
                        "price_unit": insurance.amount,
                        "account_id": income_account.id if income_account else False,
                    }),],
            }
            self.env["account.move"].create(invoice_vals)
            
    def active_inactive(self):
        for insu in self:
            if insu.state == "active":
                insu.state = "inactive"
            else:
                insu.state = "active"