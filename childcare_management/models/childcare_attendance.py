from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta,time
import pytz
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
    extra_hours = fields.Float("Horas Extra", compute="_compute_extra_hours")
    current_status = fields.Selection(
        [('in', 'En guardería'), ('out', 'Retirado')], 
        string="Estado",
        compute='_compute_status'
    )
    
    @api.depends('check_out')
    def _compute_status(self):
        for record in self:
            record.current_status = 'out' if record.check_out else 'in'

    @api.depends('check_in', 'check_out')
    def _compute_extra_hours(self):
        for record in self:
            if not record.check_in or not record.check_out:
                record.extra_hours = 0.0
                continue

            # Obtener zona horaria del usuario
            tz = record.env.user.tz or 'UTC'
            local_tz = pytz.timezone(tz)

            # Convertir fechas UTC a datetime con zona horaria
            check_in_utc = pytz.utc.localize(record.check_in)
            check_out_utc = pytz.utc.localize(record.check_out)

            # Convertir a la zona horaria del usuario
            check_in_local = check_in_utc.astimezone(local_tz)
            check_out_local = check_out_utc.astimezone(local_tz)

            if check_out_local <= check_in_local:
                record.extra_hours = 0.0
                continue

            extra_hours = 0.0
            current_date = check_in_local.date()
            end_date = check_out_local.date()

            while current_date <= end_date:
                # Calcular 6 PM del día actual en la zona horaria local
                day_start = local_tz.localize(datetime.combine(current_date, time(18, 0)))
                # Calcular medianoche del día siguiente (fin del día actual)
                next_day = current_date + timedelta(days=1)
                day_end = local_tz.localize(datetime.combine(next_day, time(0, 0)))

                # Calcular solapamiento entre el registro y el intervalo [6 PM, 12 AM]
                start = max(check_in_local, day_start)
                end = min(check_out_local, day_end)

                if start < end:
                    delta = end - start
                    extra_hours += delta.total_seconds() / 3600  # Convertir segundos a horas

                current_date = next_day  # Siguiente día

            record.extra_hours = extra_hours

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