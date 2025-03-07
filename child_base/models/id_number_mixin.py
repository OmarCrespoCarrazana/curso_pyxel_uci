# models/id_number_mixin.py
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError

class IdNumberMixin(models.AbstractModel):
    _name = 'id.number.mixin'
    _description = 'Mixin para procesar número de identificación'
    
    id_number = fields.Char("Número de Identificación", copy=False)
    dob = fields.Date("Fecha Nacimiento", compute="_compute_from_id_number", store=True)
    gender = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino')],
        "Sexo",
        compute="_compute_from_id_number",
        store=True
    )
    age = fields.Char("Edad", compute="_compute_age", store=True)

    @api.depends('id_number')
    def _compute_from_id_number(self):
        for record in self:
            id_number = record.id_number
            if not id_number:
                record.dob = False
                record.gender = False
                continue

            if not id_number.isdigit():
                raise UserError("El número de identificación debe contener solo dígitos.")

            if len(id_number) != 11:
                raise UserError("El número de identificación debe tener 11 dígitos.")

            try:
                year = int(id_number[0:2])
                month = int(id_number[2:4])
                day = int(id_number[4:6])
                century_digit = int(id_number[6])
                gender_digit = int(id_number[9]) # Only the 10th digit

                # Determine century
                if century_digit == 9:
                    year += 1800  # 19th Century
                elif 0 <= century_digit <= 5:
                    year += 1900  # 20th Century
                elif 6 <= century_digit <= 8:
                    year += 2000  # 21st Century
                else:
                    raise UserError("Dígito de siglo inválido en el número de identificación.")


                calculated_dob = date(year, month, day)

                # Check if the date is in the future
                if calculated_dob > date.today():
                    raise UserError("La fecha de nacimiento no puede ser posterior a la fecha actual.")


                record.dob = calculated_dob


                # Determine gender
                if int(gender_digit) % 2 == 0:
                    record.gender = 'male'
                else:
                    record.gender = 'female'

            except ValueError:
                raise UserError("Fecha inválida en el número de identificación.")
            except Exception as e:
                raise UserError(f"Error al procesar el número de identificación: {e}")
            
    @api.depends('dob')
    def _compute_age(self):
        """Versión básica para modelos generales"""
        for record in self:
            if not record.dob:
                record.age = "Fecha desconocida"
                continue
                
            delta = relativedelta(date.today(), record.dob)
            record.age = f"{delta.years} años"