from odoo import models, fields, api
from datetime import datetime
from odoo import http
from odoo.http import request

class HrContract(models.Model):
    _inherit = 'hr.contract'
                

    contract_code = fields.Char(string="Código de contrato", readonly=True, copy=False)
    employee_surnames = fields.Char(
        string="Apellidos",
        related='employee_id.surnames',
        store=True, 
        readonly=True
    )

    @api.model
    def create(self, vals):
        if not vals.get('contract_code'):
            year = fields.Date.today().strftime('%Y')
            last_contract = self.env['hr.contract'].search(
                [('contract_code', 'like', f"/{year}")], 
                order='contract_code DESC', 
                limit=1
            )
            if last_contract and last_contract.contract_code:
                last_seq = int(last_contract.contract_code.split('/')[0])
                new_seq = last_seq + 1
            else:
                new_seq = 1
            vals['contract_code'] = f"{new_seq}/{year}"
        return super(HrContract, self).create(vals)
    


