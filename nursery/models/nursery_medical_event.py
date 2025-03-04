from odoo import models,fields,api

class NurseryMedicalEvent(models.Model):
    _name = 'nursey.medical.event'
    _description = 'eventos médicos relacionados con los niños'

    name = fields.Char(string="Evento", required=True)
    description = fields.Char(string="Descripción del evento", required=True)
    child_hc = fields.Many2one("nursery.clinical.history",stirng="Historia clínica del niño", required=True)
    child_name = fields.Char(related='child_hc.child_id',string="Nombre del niño")
    