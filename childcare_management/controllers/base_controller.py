from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug
import logging
_logger = logging.getLogger(__name__)

class BaseController(http.Controller):

    def _prepare_page_values(self, page_name=None):
        user = request.env.user

        # Obtener el partner_id del usuario actual
        current_partner_id = user.partner_id.id
        
        # Contador de niños
        tutor_relations = request.env['childcare.child.tutor'].sudo().search([
            ('tutor_id', '=', current_partner_id)
        ])
        children_count = len(tutor_relations)
        
        # IDs de los niños asociados al usuario
        child_ids = tutor_relations.mapped('child_id.id')
        
        # Contador de historias clínicas
        medical_records = request.env['nursery.clinical.history'].sudo().search([
            ('child_id', 'in', child_ids)
        ])
        medical_records_count = len(medical_records)
        
        # Contador de eventos médicos
        medical_events_count = 0
        if medical_records:
            medical_events = request.env['nursery.medical.event'].sudo().search([
                ('id', 'in', medical_records.mapped('medical_events').ids)
            ])
            medical_events_count = len(medical_events)
        
        # Contador de facturas
        invoices = request.env['account.move'].sudo().search([
            ('partner_id', '=', current_partner_id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
        ])
        invoices_count = len(invoices)

        values = {
            'page_name': page_name,
            'children_count': children_count,
            'medical_records_count': medical_records_count,
            'medical_events_count': medical_events_count,
            'invoices_count': invoices_count,
            'user': user,
            'is_logged_in': not user._is_public() 
        }
        _logger.info("Valores pasados a la plantilla: %s", values)
        return values



    