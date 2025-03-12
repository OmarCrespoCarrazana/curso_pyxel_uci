from odoo import models, fields, api, _
from odoo.exceptions import UserError
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
        required=True
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


    @api.constrains('height', 'weight')
    def _check_positive_values(self):
        for record in self:
            if record.height <= 0:
                raise UserError("La estatura debe ser un valor positivo.")
            if record.weight <= 0:
                raise UserError("El peso debe ser un valor positivo.")
