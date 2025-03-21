from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError
from datetime import datetime

class NurseryClinicalHistory(models.Model):
    _name = "nursery.clinical.history"
    _description = "Historia Clínica de Niño"

    name = fields.Char(
        string='Code', 
        default=lambda self: self.env['ir.sequence'].next_by_code('nursery.clinical.history'),
        readonly=True,
        required=True,
        copy=False
    )
    child_id = fields.Many2one(
        "childcare.child",
        string="Niño",
        required=True,
        domain=lambda self: [
        ('id', 'not in', self.env['nursery.clinical.history'].search([]).mapped('child_id.id'))
        ],
        options={'no_create': True}  # Desactiva la opción de crear nuevo niño
    )
    date = fields.Datetime(
        string="Fecha/Hora",
        default=fields.Datetime.now,
        required=True
    )
    height = fields.Float(string="Estatura (cm)")
    weight = fields.Float(string="Peso (kg)")
    vaccines = fields.Many2many("nursery.vaccines", string="Vacunas",)
    medical_events = fields.One2many(
        "nursery.medical.event",
        "child_hc",
        string="Eventos médicos"
    )
    
    doctor_id = fields.Many2one(
        "hr.employee",
        string="Doctor",
        required=True,
        domain=[('job_id', '=', 'Doctor')]
    )

    personal_pathological_history = fields.Text(
        string="Antecedentes Patológicos Personales"
    )
    family_pathological_history = fields.Text(
        string="Antecedentes Patológicos Familiares"
    )
    general_physical_exam = fields.Text(
        string="Examen Físico General"
    )

    ophthalmology_exam_ids = fields.One2many(
    "ophthalmology.exam",
    "clinical_history_id",
    string="Exámenes de Oftalmología"
    )
    stomatology_exam_ids = fields.One2many(
        "stomatology.exam",
        "clinical_history_id",
        string="Exámenes de Estomatología"
    )
    hemogram_exam_ids = fields.One2many(
        "hemogram.exam",
        "clinical_history_id",
        string="Exámenes de Hemograma"
    )
    feces_exam_ids = fields.One2many(
        "feces.exam",
        "clinical_history_id",
        string="Exámenes de Heces Fecales"
    )
    urine_exam_ids = fields.One2many(
        "urine.exam",
        "clinical_history_id",
        string="Exámenes de Orina"
    )

    @api.constrains('child_id')
    def _check_unique_medical_history(self):
        for record in self:
            # Verificar si ya existe una historia clínica para este niño
            existing_history = self.search([
                ('child_id', '=', record.child_id.id),
                ('id', '!=', record.id)
            ])
            if existing_history:
                raise UserError(f"El niño {record.child_id.name} ya tiene una historia clínica asignada.")


    @api.constrains('height', 'weight')
    def _check_positive_values(self):
        for record in self:
            if record.height <= 0:
                raise UserError("La estatura debe ser un valor positivo.")
            if record.weight <= 0:
                raise UserError("El peso debe ser un valor positivo.")

    @api.model
    def write(self, vals):
        if self.env.user.has_group('nursery.group_nursery_nurse'):
            raise AccessError("Las enfermeras no tienen permitido modificar la información de la historia clínica.")
        return super(NurseryClinicalHistory, self).write(vals)