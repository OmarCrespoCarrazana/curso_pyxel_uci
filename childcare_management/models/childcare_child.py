from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import date, datetime

class ChildcareChild(models.Model):
    _name = "childcare.child"
    _description = "Niño en Guardería"

    name = fields.Char("Nombre", required=True)
    id_number = fields.Char("Número de Identificación")
    dob = fields.Date("Fecha de Nacimiento", compute="_compute_from_id_number", store=True)
    age = fields.Integer("Edad", compute="_compute_age", store=True)
    gender = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino')],
        string="Sexo",
        compute="_compute_from_id_number",
        store=True
    )
    classroom_id = fields.Many2one("childcare.classroom", "Aula")
    tutor_ids = fields.Many2many("res.partner", string="Tutores")
    medical_history_id = fields.Many2one(
        "childcare.medical.history",
        "Historia Clínica",
        ondelete="cascade"
    )
    attendance_ids = fields.One2many(
        "childcare.attendance",
        "child_id",
        "Asistencia"
    )


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
        for record in self:
            if record.dob:
                today = date.today()
                record.age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
            else:
                record.age = False

    
