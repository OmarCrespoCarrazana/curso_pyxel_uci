from odoo import models, fields, api

class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'

    max_capacity = fields.Integer(string="Capacidad Máxima", default=10)
   