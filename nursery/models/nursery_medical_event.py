from odoo import models,fields,api

class NurseryMedicalEvent(models.Model):
    _name = 'nursery.medical.event'
    _description = 'eventos médicos relacionados con los niños'

    name = fields.Char(string="Evento", required=True)
    description = fields.Html(string="Descripción del evento", required=True)
    child_hc = fields.Many2one("nursery.clinical.history",string="Historia clínica del niño", required=True)
    child_name = fields.Char(related="child_hc.child_id.name", readonly=True)
    used_meds = fields.Many2one("product.product", string="Medicamentos o insumos médicos empleados")
    date = fields.Date(string="Fecha", default=fields.Date.today, readonly=True)