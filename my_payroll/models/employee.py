from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    payroll_ids = fields.One2many('my_payroll.payroll', 'employee_id', string='Nóminas')