from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    childcare_children_ids = fields.One2many(
        'childcare.child.tutor', 
        'tutor_id', 
        string="Niños asociados",
        help="Niños donde este contacto es tutor"
    )