# models/hr_attendance.py
from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    overtime_hours = fields.Float(string='Overtime Hours', compute='_compute_overtime_hours', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_overtime_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                # Supongamos que la jornada laboral es de 8 horas
                regular_hours = 10.0
                worked_hours = (record.check_out - record.check_in).total_seconds() / 3600
                record.overtime_hours = max(0, worked_hours - regular_hours)
            else:
                record.overtime_hours = 0.0