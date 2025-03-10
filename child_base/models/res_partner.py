from odoo import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'id.number.mixin']
    
    childcare_children_ids = fields.One2many(
        'childcare.child.tutor', 
        'tutor_id', 
        string="Niños asociados",
        help="Niños donde este contacto es tutor"
    )