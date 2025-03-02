from odoo import models, fields, api
from datetime import datetime

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
        # Generar el código del contrato antes de crear el registro
        if not vals.get('contract_code'):
            # Obtener el año actual
            year = fields.Date.today().strftime('%Y')
            
            # Buscar el último secuencial registrado para el año actual
            last_contract = self.env['hr.contract'].search(
                [('contract_code', 'like', f"/{year}")], 
                order='contract_code DESC', 
                limit=1
            )
            if last_contract and last_contract.contract_code:
                # Extraer el número secuencial del último código
                last_seq = int(last_contract.contract_code.split('/')[0])
                new_seq = last_seq + 1
            else:
                # Si no hay registros para este año, iniciar en 1
                new_seq = 1
            
            # Asignar el nuevo código al registro
            vals['contract_code'] = f"{new_seq}/{year}"
        
        # Llamar al método create original
        return super(HrContract, self).create(vals)