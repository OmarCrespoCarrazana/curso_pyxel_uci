from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ChildcareAttendance(models.Model):
    _name = "childcare.attendance"
    _description = "Asistencia de Niños"

    name= fields.Char("Niño",related='child_id.name')
    child_id = fields.Many2one(
        "childcare.child", 
        "Niño", 
        required=True
    )
    educator_id = fields.Many2one(
        "hr.employee", 
        "Educadora", 
        default=lambda self: self.env.user.employee_id
    )
    check_in = fields.Datetime("Entrada", default=fields.Datetime.now)
    check_out = fields.Datetime("Salida")
    duration = fields.Float("Duración (horas)", compute="_compute_duration")
    current_status = fields.Selection(
        [('in', 'En guardería'), ('out', 'Retirado')], 
        string="Estado",
        compute='_compute_status'
    )
    
    @api.depends('check_out')
    def _compute_status(self):
        for record in self:
            record.current_status = 'out' if record.check_out else 'in'

    @api.onchange("check_in", "check_out")
    def _compute_duration(self):
        for record in self:
            if record.check_out and record.check_in:
                delta = record.check_out - record.check_in
                record.duration = delta.total_seconds() / 3600
            else:
                record.duration = 0

    def button_set_check_out(self):
        self.ensure_one()
        current_time = fields.Datetime.now()
        self.write({
            'check_out': current_time,
            
        })

    """   def button_set_check_in(self):
        self.ensure_one()
        current_time = fields.Datetime.now()
        self.write({
            'check_in': current_time,
            'check_out': False  
        })"""
    @api.constrains('check_in', 'check_out')
    def _check_valid_times(self):
        for record in self:
            if record.check_out and record.check_in:
                if record.check_out < record.check_in:
                    raise ValidationError("La hora de salida no puede ser anterior a la entrada")
                
                if record.check_in > datetime.now():
                    raise ValidationError("No se puede registrar una entrada futura")