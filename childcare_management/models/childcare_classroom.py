from odoo import models, fields, api, exceptions

class ChildcareClassroom(models.Model):
    _name = "childcare.classroom"
    _description = "Aula de Guardería"

    name = fields.Char("Nombre", required=True)
    capacity = fields.Integer("Capacidad Máxima", default=10)
    educator_id = fields.Many2one(
        "hr.employee", 
        "Educadora",
        domain="[('classroom_id', '=', False)]",  
        unique=True  
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

    @api.model
    def create(self, vals):
        # Crear el aula y sincronizar educator_id -> classroom_id
        classroom = super(ChildcareClassroom, self).create(vals)
        if 'educator_id' in vals and not self.env.context.get('syncing_educator'):
            educator = self.env['hr.employee'].browse(vals['educator_id'])
            if educator:
                educator.with_context(syncing_educator=True).write({'classroom_id': classroom.id})
        return classroom
    
    def unlink(self):
        for record in self:
            if record.child_ids:
                raise exceptions.UserError("No se puede eliminar el aula porque tiene niños asignados.  Primero, retire los niños del aula.")
        return super(ChildcareClassroom, self).unlink()
    @api.depends('child_ids')
    def _compute_child_count(self):
        for classroom in self:
            classroom.child_count = len(classroom.child_ids)

    def write(self, vals):
        # Actualizar classroom_id en el empleado cuando se cambia educator_id
        if 'educator_id' in vals and not self.env.context.get('syncing_educator'):
            for classroom in self:
                # Educadora anterior
                old_educator = classroom.educator_id
                # Educadora nueva
                new_educator = self.env['hr.employee'].browse(vals['educator_id']) if vals['educator_id'] else None

                # Quitar aula de la educadora anterior
                if old_educator:
                    old_educator.with_context(syncing_educator=True).write({'classroom_id': False})

                # Asignar aula a la educadora nueva
                if new_educator:
                    new_educator.with_context(syncing_educator=True).write({'classroom_id': classroom.id})

        return super(ChildcareClassroom, self).write(vals)