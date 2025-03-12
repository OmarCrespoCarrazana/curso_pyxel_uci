from odoo import models,fields,api
from odoo.exceptions import UserError

class NurseryMedicalEvent(models.Model):
    _name = 'nursery.medical.event'
    _description = 'eventos médicos relacionados con los niños'

    name = fields.Char(string="Evento", required=True)
    description = fields.Html(string="Descripción del evento", required=True)
    child_hc = fields.Many2one("nursery.clinical.history",string="Historia clínica del niño", required=True)
    child_name = fields.Char(related="child_hc.child_id.name", readonly=True)
    used_meds = fields.Many2one("product.product", string="Medicamentos o insumos médicos empleados")
    date = fields.Date(string="Fecha", default=fields.Date.today, readonly=True)

    @api.model
    def create(self, vals):
        # Validación: Si se crea desde el contexto, asigna y bloquea el campo child_hc
        if not vals.get('child_hc') and self.env.context.get('default_child_hc'):
            vals['child_hc'] = self.env.context['default_child_hc']
        elif not vals.get('child_hc'):
            raise UserError("Debe seleccionar una Historia Clínica para el evento médico.")
        
        # Lógica principal para crear el registro del evento
        record = super(NurseryMedicalEvent, self).create(vals)

        # Enviar notificación por correo electrónico
        if record.child_hc.child_id.tutor_ids:
            tutors = record.child_hc.child_id.tutor_ids
            template = self.env.ref('nursery.email_template_medical_event_notification', raise_if_not_found=False)
            if not template:
                raise UserError("No se encontró la plantilla de correo para notificaciones de eventos médicos.")
            
            for tutor in tutors:
                template.send_mail(record.id, email_values={'email_to': tutor.email}, force_send=True)

        return record
    
    def default_get(self, fields_list):
        res = super(NurseryMedicalEvent, self).default_get(fields_list)
        # Asignar automáticamente el valor del contexto si existe
        if self.env.context.get('default_child_hc'):
            res['child_hc'] = self.env.context['default_child_hc']
        return res

    @api.onchange('child_hc')
    def _onchange_child_hc(self):
        # Bloqueo dinámico: Evitar cambios si viene del contexto
        if self.env.context.get('default_child_hc') and self.child_hc:
            raise UserError("No puedes modificar el campo 'Historia Clínica' cuando se crea desde una historia clínica.")
        
    @api.model
    def create(self, vals):
        user = self.env.user
        # Validar contexto para restringir la creación desde dentro de la historia clínica
        if user.has_group('nursery.group_nursery_nurse') and self.env.context.get('default_child_hc'):
            raise UserError("Las enfermeras no pueden crear eventos médicos desde una historia clínica.")
        return super(NurseryMedicalEvent, self).create(vals)