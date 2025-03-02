from odoo import models, fields, api


class NurseryMedicalSupply(models.Model):
    _name = 'nursery.medical.supply'
    _description = 'Suministros médicos para guarderías'

    product_id = fields.Many2one(
        'product.product',
        string="Producto",
        required="true"
    )
    min_quantity = fields.Float(
        string="Cantidad mínima",
        required="true"
    )
    current_quantity = fields.Float(
        string="Cantidad en existencia",
        readonly=True,
    )
    alert = fields.Boolean(
        string="Alerta",
    )

    @api.onchange('current_quantity')
    def _check_alert(self):

        for record in self:
            if record.current_quantity <= record.min_quantity:
                record.alert = True
            else:
                record.alert = False