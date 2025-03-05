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
        store=True,  # Guarda el valor en la base de datos si es necesario
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
    


"""    

    def get_contracts_data(self):
        
        contracts_data = []
        for contract in self:
            contracts_data.append({
                'contract_code': contract.contract_code or 'N/A',
                'employee_name': contract.employee_id.name if contract.employee_id else 'N/A',
                'employee_surnames': contract.employee_surnames or 'N/A',
                'name': contract.name or 'N/A',
                'date_start': contract.date_start.strftime('%Y-%m-%d') if contract.date_start else 'N/A',
                'date_end': contract.date_end.strftime('%Y-%m-%d') if contract.date_end else 'N/A',
                'wage': contract.wage or 'N/A',
            })

        # Pasar los datos como contexto
        return self.env.ref('employee.action_report_contract').report_action(
            self,
            data={'contracts_data': contracts_data}
        )


class ContractReportController(http.Controller):

    @http.route('/contracts/report', type='http', auth='user')
    def contract_report(self):
        # Obtener todos los contratos
        contracts = request.env['hr.contract'].search([])

        # Obtener los datos del reporte usando el método del modelo
        contracts_data = contracts.get_contracts_data()

        # Renderizar la plantilla QWeb con los datos
        return request.render('employee.hr_contract_report', {
            'contracts_data': contracts_data,
        })

    """