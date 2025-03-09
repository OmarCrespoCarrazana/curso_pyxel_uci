from odoo import models, fields, api, exceptions


class ChildcareChild(models.Model):
    _inherit = 'childcare.child'
    


    classroom_id = fields.Many2one("childcare.classroom", "Aula")

    attendance_ids = fields.One2many(
        "childcare.attendance",
        "child_id",
        "Asistencia"
    )
    
    total_extra_hours = fields.Float(
        string="Horas Extra Totales",
        compute="_compute_total_extra_hours",
        store=True,  
        help="Total de horas extra acumuladas por el niño."
    )
    medical_history_id = fields.One2many(
        "nursery.clinical.history", 
        "child_id",  
        string="Historia Clínica",  
        ondelete="cascade"
    )
    medical_history_height = fields.Float(
        related='medical_history_id.height',
        string="Estatura (cm)",
        readonly=True  
    )
    medical_history_weight = fields.Float(
        related='medical_history_id.weight',
        string="Peso (kg)",
        readonly=True
    )
    medical_history_vaccines = fields.Many2many(
        related='medical_history_id.vaccines',
        string="Vacunas",
        readonly=True
    )
    medical_history_doctor_id = fields.Many2one(
        related='medical_history_id.doctor_id',
        string="Doctor",
        readonly=True
    )
    @api.constrains("classroom_id")
    def _check_capacity(self):
        for classroom in self.classroom_id:
            if len(classroom.child_ids) > classroom.capacity:
                raise exceptions.ValidationError(
                    "El aula excede su capacidad máxima"
                )

    @api.depends('attendance_ids.extra_hours')  
    def _compute_total_extra_hours(self):
        for child in self:
            # Sumar todas las horas extra de los registros de asistencia del niño
            child.total_extra_hours = sum(child.attendance_ids.mapped('extra_hours'))
    
    def action_contact_tutors(self):
        self.ensure_one()
        domain = repr([('id', 'in', self.tutor_ids.ids)])
        
        return {
            'name': ('Contactar Tutores'),
            'type': 'ir.actions.act_window',
            'res_model': 'mailing.mailing',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_mailing_model_id': self.env.ref('base.model_res_partner').id,
                'default_mailing_domain': domain,
            },
        }
    
    def action_assign_best_classroom(self):
        self.ensure_one()  
        classrooms = self.env['childcare.classroom'].search([])
        available_classrooms = classrooms.filtered(lambda c: c.child_count < c.capacity)
        
        if not available_classrooms:
            raise exceptions.UserError("¡No hay aulas disponibles con capacidad suficiente!")
                
        sorted_classrooms = available_classrooms.sorted(
            key=lambda c: (c.child_count, -c.capacity)
        )                
        self.classroom_id = sorted_classrooms[0]