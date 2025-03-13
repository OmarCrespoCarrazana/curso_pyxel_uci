# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
from .base_controller import BaseController
from odoo.tools import image_data_uri
import logging
_logger = logging.getLogger(__name__)

class ChildcarePortal(BaseController):

    def _get_children_data(self):
        """Fetch children data from the database, filtered by the current user's partner_id"""
        # Get current user's partner_id
        current_partner_id = request.env.user.partner_id.id
        
        # Buscar los registros de relación donde el partner actual es tutor
        tutor_relations = request.env['childcare.child.tutor'].sudo().search([
            ('tutor_id', '=', current_partner_id)
        ])
        
        # Extraer los IDs de los niños relacionados
        child_ids = tutor_relations.mapped('child_id.id')
        
        # Obtener los registros completos de los niños
        children_records = request.env['childcare.child'].sudo().browse(child_ids)
        
        _logger.info(f"Found {len(children_records)} children for partner_id {current_partner_id}")
        
        children_data = []
        
        default_images = {
            'male': '/childcare_management/static/src/img/child-placeholder-male.jpg',
            'female': '/childcare_management/static/src/img/child-placeholder-female.jpg'
        }
        
        for child in children_records:
            # Get classroom data

            classroom_data = None
            if child.classroom_id:
                classroom_data = {
                    'id': child.classroom_id.id,
                    'name': child.classroom_id.name
                }
            
            # Get tutors data - usando la relación muchos a muchos a través del modelo intermedio
            tutors_data = []
            for tutor_relation in child.tutor_ids:
                tutor = tutor_relation.tutor_id
                tutors_data.append({
                    'id': tutor.id,
                    'name': tutor.name,
                    'email': tutor.email,
                    'phone': tutor.phone
                })
            
            # Get medical history data
            medical_history_data = None
            if child.medical_history_id:
                medical_history = child.medical_history_id[0] if child.medical_history_id else None
                if medical_history:
                    medical_history_data = {
                        'height': medical_history.height,
                        'weight': medical_history.weight,
                        'vaccines': ', '.join(medical_history.vaccines.mapped('name')),
                        'doctor_id': {
                            'id': medical_history.doctor_id.id,
                            'name': medical_history.doctor_id.name
                        } if medical_history.doctor_id else None
                    }
            
            # Get attendance data
            attendance_data = []
            for attendance in child.attendance_ids:
                attendance_data.append({
                    'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_in else '',
                    'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_out else '',
                    'extra_hours': attendance.extra_hours
                })
            
            # Calculate age - usando el campo calculado 'age' si está disponible
            age_str = child.age if hasattr(child, 'age') and child.age else "Desconocido"
            # Extraer el número de años del string "X años y Y meses"
            if isinstance(age_str, str) and "año" in age_str:
                age = int(age_str.split(" ")[0])
            else:
                age = 0
            image_url = None
            if child.image and isinstance(child.image, bytes):  # Asegurar que es un binario válido
                image_url = image_data_uri(child.image)
            # Build child data dictionary
            child_data = {
                'id': child.id,
                'name': child.name,
                'id_number': child.id_number if hasattr(child, 'id_number') else '',
                'dob': child.dob.strftime('%Y-%m-%d') if child.dob else '',
                'age': age,
                'gender': child.gender,
                'classroom_id': classroom_data,
                'tutor_ids': tutors_data,
                'medical_history_id': medical_history_data,
                'attendance_ids': attendance_data,
                'total_extra_hours': child.total_extra_hours if hasattr(child, 'total_extra_hours') else 0,
                'photo_url': image_url if image_url else None
            }
            _logger.info(f"Imagen URL para {child.name}: {image_url}")
            
            
            children_data.append(child_data)
        
        return children_data

    @http.route(['/childcare'], type='http', auth='user', website=True)
    def portal_childcare_home(self, **kw):
        values = self._prepare_page_values('children')
        # Add children data
        values.update({
            'children_data': self._get_children_data(),
            'default_images': {
                'male': '/childcare_management/static/src/img/child-placeholder-male.jpg',
                'female': '/childcare_management/static/src/img/child-placeholder-female.jpg'
            }
        })
        return request.render("childcare_management.children_page", values)
    
    @http.route(['/childcare/<int:child_id>'], type='http', auth='user', website=True)
    def child_detail(self, child_id, **kw):
        """Shows details of a specific child with security check"""
        values = self._prepare_page_values('child_detail')
        
        # Get current user's partner_id
        current_partner_id = request.env.user.partner_id.id
        
        # Verificar si el usuario actual es tutor de este niño
        tutor_relation = request.env['childcare.child.tutor'].sudo().search([
            ('child_id', '=', child_id),
            ('tutor_id', '=', current_partner_id)
        ], limit=1)
        
        # Security check - if the current user is not a tutor for this child, redirect
        if not tutor_relation:
            _logger.warning(f"Security: Partner {current_partner_id} attempted to access child {child_id} without permission")
            return request.redirect('/childcare')
            
        # Obtener el registro del niño
        child_record = request.env['childcare.child'].sudo().browse(child_id)
        if not child_record.exists():
            return request.redirect('/childcare')
        
        # Get all data for this child in the expected format
        # Get classroom data
        classroom_data = None
        if child_record.classroom_id:
            classroom_data = {
                'id': child_record.classroom_id.id,
                'name': child_record.classroom_id.name
            }
        
        # Get tutors data
        tutors_data = []
        for tutor_relation in child_record.tutor_ids:
            tutor = tutor_relation.tutor_id
            tutors_data.append({
                'id': tutor.id,
                'name': tutor.name,
                'email': tutor.email,
                'phone': tutor.phone
            })
        
        # Get medical history data
        medical_history_data = None
        if child_record.medical_history_id:
            medical_history = child_record.medical_history_id[0] if child_record.medical_history_id else None
            if medical_history:
                medical_history_data = {
                    'height': medical_history.height,
                    'weight': medical_history.weight,
                    'vaccines': ', '.join(medical_history.vaccines.mapped('name')),
                    'doctor_id': {
                        'id': medical_history.doctor_id.id,
                        'name': medical_history.doctor_id.name
                    } if medical_history.doctor_id else None
                }
        
        # Get attendance data
        attendance_data = []
        for attendance in child_record.attendance_ids:
            attendance_data.append({
                'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_in else '',
                'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S') if attendance.check_out else '',
                'extra_hours': attendance.extra_hours
            })
        
        # Calculate age - usando el campo calculado 'age' si está disponible
        age_str = child_record.age if hasattr(child_record, 'age') and child_record.age else "Desconocido"
        # Extraer el número de años del string "X años y Y meses"
        if isinstance(age_str, str) and "año" in age_str:
            age = int(age_str.split(" ")[0])
        else:
            age = 0
        
        # Build child data dictionary
        child = {
            'id': child_record.id,
            'name': child_record.name,
            'id_number': child_record.id_number if hasattr(child_record, 'id_number') else '',
            'dob': child_record.dob.strftime('%Y-%m-%d') if child_record.dob else '',
            'age': age,
            'gender': child_record.gender,
            'classroom_id': classroom_data,
            'tutor_ids': tutors_data,
            'medical_history_id': medical_history_data,
            'attendance_ids': attendance_data,
            'total_extra_hours': child_record.total_extra_hours if hasattr(child_record, 'total_extra_hours') else 0,
            'photo_url': child_record.image if hasattr(child_record, 'image') and child_record.image else None
        }
        
        values.update({
            'child': child,
            'default_images': {
                'male': '/childcare_management/static/src/img/child-placeholder-male.jpg',
                'female': '/childcare_management/static/src/img/child-placeholder-female.jpg'
            }
        })
        
        return request.render("childcare_management.child_detail_page", values)
    
        
    @http.route(['/request-service'], type='json', auth='user', website=True)
    def create_service(self, name, id_number, **kw):
        try:
            # Obtener el partner del usuario actual
            user_partner = request.env.user.partner_id
            
            # Crear primero el niño
            child_vals = {
                'name': name,
                'id_number': id_number,
            }
            
            child = request.env['childcare.child'].sudo().create(child_vals)
            
            # Crear la relación tutor-niño con el usuario actual como padre
            tutor_relation_vals = {
                'child_id': child.id,
                'tutor_id': user_partner.id,
                'relationship': 'Padre',  # Relación por defecto
                'is_legal_guardian': True  # Por defecto, marcar como tutor legal
            }
            
            tutor_relation = request.env['childcare.child.tutor'].sudo().create(tutor_relation_vals)
            # Crear un lead y vincularlo con el niño
            lead_vals = {
                'name': f"Childcare service for {name}",
                'partner_id': user_partner.id,
                'child_id': child.id,
                'type': 'opportunity',  # Assuming you want to create it as an opportunity
                'description': f"Childcare service request for {name} (ID: {id_number}) " 
                            f"created from the web portal by {user_partner.name}."
            }
            lead = request.env['crm.lead'].sudo().create(lead_vals)

            _logger.info(f"Child created: {name}, {id_number}, ID: {child.id}, Partner: {user_partner.id}, Lead: {lead.id}")
        
            return {
                'status': 200,
                'message': 'Child created successfully',
                'child_id': child.id,
                'lead_id': lead.id
            }

        except ValidationError as ve:
            _logger.error(f"Validation error creating child: {str(ve)}")
            return {
                'status': 400,
                'message': str(ve),
                'field': 'id_number'  
            }
        except UserError as ue:
            _logger.error(f"User error creating child: {str(ue)}")
            return {
                'status': 400,
                'message': str(ue),
                'field': 'id_number'
            }
        except Exception as e:
            _logger.error(f"Error creating child: {str(e)}")
            return {
                'status': 500,
                'message': f'Error creating child: {str(e)}'
            }