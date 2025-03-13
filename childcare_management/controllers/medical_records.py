# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
from .base_controller import BaseController
import logging
_logger = logging.getLogger(__name__)

class MedicalRecords(BaseController):
    @http.route(['/medical-records/<int:child_id>'], type='http', auth='user', website=True)
    def portal_medical_records(self, child_id, **kw):
        _logger.info("Medical Records Page %s", child_id)
        values = self._prepare_page_values('medical')
        values['child_id'] = child_id
        return request.render("childcare_management.medical_records_page", values)        
      
    @http.route(['/medical-records_json'], type='json', auth='user', website=True)
    def get_records(self, child_id, **kw):
        try:
            child_id = int(child_id)
            _logger.info("Fetching Medical Records for child ID %s", child_id)

           
            child_record = request.env['childcare.child'].sudo().browse(child_id)
            base_child_data = {
                'id': child_id,
                'name': child_record.name if child_record.exists() else 'Unknown Child',
                'height': 0.0,
                'weight': 0.0
            }
            # 1. Obtener historia clínica del niño
            clinical_records = request.env['nursery.clinical.history'].search_read(
                [('child_id', '=', child_id)],
                ['date', 'child_id', 'doctor_id', 'height', 'weight', 'vaccines', 'medical_events'],
                order='date desc'
            )
            
            if not clinical_records:
                return {
                    'status': 200,
                    'records': [{
                        'child': base_child_data,
                        'doctor': None,
                        'vaccines': [],
                        'medical_events': []
                    }]
                }
            
            # 2. Extraer IDs de relaciones
            doctor_ids = list(set([record['doctor_id'][0] for record in clinical_records if record.get('doctor_id')]))
            vaccine_ids = []
            event_ids = []
            
            for record in clinical_records:
                if record.get('vaccines'):
                    vaccine_ids.extend(record['vaccines'])
                if record.get('medical_events'):
                    event_ids.extend(record['medical_events'])
            
            vaccine_ids = list(set(vaccine_ids))
            event_ids = list(set(event_ids))
            
            # 3. Obtener datos relacionados
            doctors = request.env['hr.employee'].search_read(
                [('id', 'in', doctor_ids)],
                ['name', 'work_phone', 'work_email']
            )
            
            vaccines = request.env['nursery.vaccines'].search_read(
                [('id', 'in', vaccine_ids)],
                ['name']
            )
            
            medical_events = request.env['nursery.medical.event'].search_read(
                [('id', 'in', event_ids)],
                ['name', 'description', 'date', 'used_meds', 'child_name']
            )
            
            # 4. Obtener productos/medicamentos utilizados
            med_ids = [event['used_meds'][0] for event in medical_events 
                      if event.get('used_meds') and event['used_meds']]
            
            products = request.env['product.product'].search_read(
                [('id', 'in', med_ids)],
                ['name']
            )
            
            # 5. Crear diccionarios para búsqueda rápida
            doctor_dict = {d['id']: d for d in doctors}
            vaccine_dict = {v['id']: v for v in vaccines}
            event_dict = {e['id']: e for e in medical_events}
            product_dict = {p['id']: p for p in products}
            
            # 6. Procesar y estructurar los datos para el frontend
            processed_records = []
            for record in clinical_records:
                # Datos del niño (id, nombre, height, weight)
                child_data = {
                    'id': base_child_data['id'],
                    'name': base_child_data['name'],
                    'height': record.get('height', base_child_data['height']),
                    'weight': record.get('weight', base_child_data['weight'])
                }
                # Datos del doctor
                doctor_data = {'name': 'Unknown', 'work_email': '', 'work_phone': ''}
                # Datos del doctor
                doctor_data = {'name': 'Unknown', 'work_email': '', 'work_phone': ''}
                if record.get('doctor_id'):
                    doctor = doctor_dict.get(record['doctor_id'][0], {})
                    doctor_data = {
                        'name': doctor.get('name', 'Unknown'),
                        'work_email': doctor.get('work_email', ''),
                        'work_phone': doctor.get('work_phone', '')
                    }
                
                # Vacunas
                vaccine_names = []
                if record.get('vaccines'):
                    for vac_id in record['vaccines']:
                        if vac_id in vaccine_dict:
                            vaccine_names.append(vaccine_dict[vac_id]['name'])
                
                # Eventos médicos con detalles completos
                detailed_events = []
                if record.get('medical_events'):
                    for event_id in record['medical_events']:
                        if event_id in event_dict:
                            event = event_dict[event_id]
                            medication_name = '-'
                            if event.get('used_meds') and event['used_meds']:
                                med_id = event['used_meds'][0]
                                if med_id in product_dict:
                                    medication_name = product_dict[med_id]['name']
                            
                            detailed_events.append({
                                'id': event_id,
                                'name': event.get('name', ''),
                                'description': event.get('description', ''),
                                'date': event.get('date', ''),
                                'child_name': event.get('child_name', ''),
                                'medication': medication_name
                            })
                
                # Construir el registro procesado
                processed_record = {
                    'id': record.get('id'),
                    'date': record.get('date'),
                    'child': child_data,
                    'doctor': doctor_data,
                    'vaccines': vaccine_names,
                    'medical_events': detailed_events
                }
                processed_records.append(processed_record)
            
            return {'status': 200, 'records': processed_records}
            
        except Exception as e:
            _logger.error("Error fetching medical records: %s", str(e))
            return {
                'status': 500, 
                'error': str(e),
                'records': [{
                    'child': base_child_data,
                    'doctor': None,
                    'vaccines': [],
                    'medical_events': []
                }]
            }