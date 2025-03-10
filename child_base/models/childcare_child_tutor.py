from odoo import models, fields, api, exceptions

class ChildcareChildTutor(models.Model):
    _name = "childcare.child.tutor"
    _description = "Relación de Tutor con Niño"

    child_id = fields.Many2one("childcare.child", required=True)
    tutor_id = fields.Many2one("res.partner", required=True, string="Tutor",domain=[('is_company', '=', False)])
    relationship = fields.Char(string="Parentesco", required=True)
    is_legal_guardian = fields.Boolean(string="Tutor Legal")