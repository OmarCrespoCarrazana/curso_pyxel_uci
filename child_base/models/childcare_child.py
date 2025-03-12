from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class ChildcareChild(models.Model):
    _name = "childcare.child"
    _description = "Niño en Guardería"
    _inherit="id.number.mixin"
    name = fields.Char("Nombre", required=True)
    image = fields.Image(
        string="Foto del Niño",
        max_width=1920,
        max_height=1920,
        help="Foto de perfil del niño"
    )
    
    #Modelo que guarda la relación entre el niño y sus tutores
    tutor_ids = fields.One2many(
        "childcare.child.tutor", 
        "child_id", 
        string="Relación Tutores"
    )
    
    legal_guardian_ids = fields.Many2many(
        "res.partner",
        compute="_compute_legal_guardians",
        string="Tutores Legales",
        store=True
    )
    possible_guardian_ids = fields.Many2many(
        "res.partner",
        compute='_compute_possible_guardian_ids',string="Tutores",store=False,readonly=True  
    )

   

   
    @api.depends('tutor_ids')
    def _compute_possible_guardian_ids(self):
         for record in self:
            record.possible_guardian_ids = record.tutor_ids.mapped('tutor_id')

    @api.depends('tutor_ids.is_legal_guardian')
    def _compute_legal_guardians(self):
        for record in self:
            record.legal_guardian_ids = record.tutor_ids.filtered(
                lambda t: t.is_legal_guardian
            ).mapped('tutor_id')

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
                    raise exceptions.ValidationError("Dígito de siglo inválido en el número de identificación.")


                calculated_dob = date(year, month, day)

                # Check if the date is in the future
                if calculated_dob > date.today():
                    raise exceptions.ValidationError("La fecha de nacimiento no puede ser posterior a la fecha actual.")


                record.dob = calculated_dob


                # Determine gender
                if int(gender_digit) % 2 == 0:
                    record.gender = 'male'
                else:
                    record.gender = 'female'

            except ValueError:
                raise exceptions.ValidationError("Fecha inválida en el número de identificación.")
            except Exception as e:
                raise exceptions.ValidationError(f"Error al procesar el número de identificación: {e}")

    @api.constrains('id_number')
    def _check_unique_id_number(self):
        for rec in self:
            if rec.id_number:
                existing = self.env['childcare.child'].search([
                    ('id_number', '=', rec.id_number),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise exceptions.ValidationError("Ya existe un niño registrado con este número de carnet de identidad.")

    @api.depends('dob')
    def _compute_age(self):
        """Versión especializada para niños con meses y validación"""
        for record in self:
            if not record.dob:
                record.age = "Fecha de nacimiento desconocida"
                return
                
            today = date.today()
            delta = relativedelta(today, record.dob)
            
            years = delta.years
            months = delta.months
            
            # Construcción del string
            age_parts = []
            if years > 0:
                age_parts.append(f"{years} año{'s' if years != 1 else ''}")
            if months > 0:
                age_parts.append(f"{months} mes{'es' if months != 1 else ''}")
            
            record.age = " y ".join(age_parts) if age_parts else "Recién nacido"
  
    @api.constrains('dob')
    def _check_max_age(self):
        """Validación específica para niños"""
        for record in self:
            if record.dob:
                delta = relativedelta(date.today(), record.dob)
                if delta.years >= 5:
                    raise exceptions.ValidationError(
                        "Edad máxima permitida es 5 años"
                    )
 
    @api.constrains('tutor_ids')
    def _check_unique_tutors(self):
        for record in self:
            tutor_ids = []
            duplicates = []
            
            for tutor in record.tutor_ids:
                if tutor.tutor_id.id in tutor_ids:
                    duplicates.append(tutor.tutor_id.name)
                else:
                    tutor_ids.append(tutor.tutor_id.id)
            
            if duplicates:
                raise exceptions.ValidationError("No se puede repetir el mismo tutor")