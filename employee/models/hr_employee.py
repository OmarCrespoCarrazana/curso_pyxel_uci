from odoo import models, fields, api
from datetime import datetime

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    id_empleado = fields.Char(string="ID Empleado", readonly=True, copy=False)
    surnames =  fields.Char(string='Apellidos')
    

    @api.model
    def create(self, vals):
        # Generar el ID de empleado antes de crear el registro
        if not vals.get('id_empleado'):
            # Obtener el año y mes actual
            year = fields.Date.today().strftime('%y')  # Año en formato corto (ej. 25 para 2025)
            month = fields.Date.today().strftime('%m')  # Mes en formato de dos dígitos
            
            # Buscar el último secuencial registrado para el año/mes actual
            last_employee = self.env['hr.employee'].search(
                [('id_empleado', 'like', f"{year}{month}")], 
                order='id_empleado DESC', 
                limit=1
            )
            if last_employee and last_employee.id_empleado:
                # Extraer el número secuencial del último ID
                last_seq = int(last_employee.id_empleado[4:])  # Extraer todo después de los primeros 4 caracteres
                new_seq = last_seq + 1
            else:
                # Si no hay registros para este mes, iniciar en 1
                new_seq = 1
            
            # Asignar el nuevo ID al registro
            vals['id_empleado'] = f"{year}{month}{new_seq}"
        
        # Llamar al método create original
        return super(HrEmployee, self).create(vals)
    
