from odoo import models, fields, api

class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'

    max_capacity = fields.Integer(string="Capacidad Máxima", default=10)
    allowed_job_positions = fields.Many2many(
        'hr.job',
        string="Puestos de trabajo permitidos",
        help="Puestos de trabajo permitidos en esta ubicación."
    )