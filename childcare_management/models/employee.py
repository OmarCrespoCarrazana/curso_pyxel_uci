# models/hr_employee.py
from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    classroom_id = fields.Many2one(
        'childcare.classroom',
        string="Aula asignada",
        domain="[('educator_id', '=', False)]",  
        unique=True  
    )
    is_educator = fields.Boolean(
        string="Es Educadora",
        compute='_compute_is_educator',
        store=True
    )
    
    @api.depends('job_id')
    def _compute_is_educator(self):
        for employee in self:
            employee.is_educator = employee.job_id.name == 'Educadora'
    
    def write(self, vals):
        # Actualizar educator_id en el aula cuando se cambia classroom_id
        if 'classroom_id' in vals and not self.env.context.get('syncing_educator'):
            for employee in self:
                # Aula anterior
                old_classroom = employee.classroom_id
                # Aula nueva
                new_classroom = self.env['childcare.classroom'].browse(vals['classroom_id']) if vals['classroom_id'] else None

                # Quitar educator_id del aula anterior
                if old_classroom:
                    old_classroom.with_context(syncing_educator=True).write({'educator_id': False})

                # Asignar educator_id al aula nueva
                if new_classroom:
                    new_classroom.with_context(syncing_educator=True).write({'educator_id': employee.id})

        return super(HrEmployee, self).write(vals)