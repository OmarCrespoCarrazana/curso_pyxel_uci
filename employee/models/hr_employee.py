from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
import re

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    id_empleado = fields.Char(string="ID Empleado", readonly=True, copy=False)
    surnames =  fields.Char(string='Apellidos')
    age = fields.Integer(string="Edad", compute="_compute_age", store=True)
    

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                # Obtener la fecha actual
                today = datetime.today()
                # Convertir la fecha de nacimiento a un objeto datetime
                birth_date = fields.Date.from_string(record.birthday)
                # Calcular la diferencia en años
                age = today.year - birth_date.year
                # Ajustar si el cumpleaños aún no ha ocurrido este año
                if (today.month, today.day) < (birth_date.month, birth_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0

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
    
    
    @api.constrains('work_location_id')
    def _check_work_location_capacity(self):
        for employee in self:
            if employee.work_location_id:
                location = employee.work_location_id
                # Contar cuántos empleados están asignados a esta ubicación
                employee_count = self.env['hr.employee'].search_count([('work_location_id', '=', location.id)])
                if employee_count > location.max_capacity:
                    raise ValidationError(
                        f"La ubicación {location.name} ha alcanzado su capacidad máxima de {location.max_capacity} empleados."
                    )
    @api.constrains('work_location_id', 'job_id')
    def _check_job_location(self):
        for employee in self:
            if employee.work_location_id and employee.job_id:
                allowed_jobs = employee.work_location_id.allowed_job_positions
                if employee.job_id not in allowed_jobs:
                    raise ValidationError(
                        "El puesto de trabajo no está permitido en esta ubicación."
                    )
    
    @api.constrains('name', 'surnames', 'identification_id')
    def _check_employee_data(self):
        for employee in self:
            # Validación del nombre
            if not employee.name or len(employee.name.strip()) < 2:
                raise ValidationError("El nombre del empleado es obligatorio y debe tener al menos 2 caracteres.")
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", employee.name.strip()):
                raise ValidationError("El nombre no puede contener números ni caracteres especiales.")

            # Validación de los apellidos
            if not employee.surnames or len(employee.surnames.strip()) < 2:
                raise ValidationError("Los apellidos del empleado son obligatorios y deben tener al menos 2 caracteres.")
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", employee.surnames.strip()):
                raise ValidationError("Los apellidos no pueden contener números ni caracteres especiales.")

            # Validación del número de identificación
            if not employee.identification_id or len(employee.identification_id) != 11 or not employee.identification_id.isdigit():
                raise ValidationError("El número de identificación debe tener exactamente 11 dígitos.")