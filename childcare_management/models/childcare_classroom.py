from odoo import models, fields, api, exceptions

class ChildcareClassroom(models.Model):
    _name = "childcare.classroom"
    _description = "Aula de Guardería"

    name = fields.Char("Nombre", required=True)
    capacity = fields.Integer("Capacidad Máxima", default=10)
    educator_id = fields.Many2one(
        "hr.employee", 
        "Educadora"
       
    )
    child_ids = fields.One2many(
        "childcare.child", 
        "classroom_id", 
        "Niños"
    )
    child_count = fields.Integer(
        string="Niños inscritos", 
        compute='_compute_child_count', 
        store=True
    )
    
    @api.depends('child_ids')
    def _compute_child_count(self):
        for classroom in self:
            classroom.child_count = len(classroom.child_ids)

  