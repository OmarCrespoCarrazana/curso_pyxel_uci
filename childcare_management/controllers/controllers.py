# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError


class ChildcarePortal(http.Controller):
    def _prepare_page_values(self, page_name=None):
        user = request.env.user
        values = {
            'page_name': page_name,
            'children_count': 3,
            'medical_records_count': 8,
            'active_services_count': 2,
            'user': user,
            'is_logged_in': not user._is_public()  # Nuevas variables añadidas
        }
        return values
    
    @http.route(['/'], type='http', auth='public', website=True)
    def childcare_home(self, **kw):
        values = self._prepare_page_values('home')
        return request.render("childcare_management.childcare_home", values)

    @http.route(['/childcare'], type='http', auth='user', website=True)
    def portal_childcare_home(self, **kw):
        values = self._prepare_page_values('children')
        return request.render("childcare_management.children_page", values)

    @http.route(['/medical-records'], type='http', auth='user', website=True)
    def portal_medical_records(self, **kw):

        medical_records = [{
            "date": "2024-01-15",
            "child": "John Doe",
            "type": "Regular Checkup",
            "description": "Annual health examination",
            "status": "completed"
        }, {
            "date": "2024-02-01",
            "child": "Jane Doe", 
            "type": "Vaccination",
            "description": "Flu shot",
            "status": "pending"
        }, {
            "date": "2024-01-20",
            "child": "Mike Smith",
            "type": "Emergency",
            "description": "Minor injury treatment",
            "status": "completed"
        }] 
        values = self._prepare_page_values('medical')
        values['medical_records'] = medical_records
        return request.render("childcare_management.medical_records_page", values)

    @http.route(['/create-service'], type='http', auth='user', website=True, methods=['POST'])
    def create_service(self, **kw):
        # Aquí procesaría los datos del formulario
        # Por ahora, solo mostraremos los datos recibidos y redirigiremos
        # Por ejemplo:
        # service_vals = {
        #     'name': kw.get('name'),
        #     'child_id': int(kw.get('child')),
        #     'start_date': kw.get('start_date'),
        #     'status': kw.get('status')
        # }
        # new_service = request.env['childcare.service'].sudo().create(service_vals)
        
        # Mostrar mensaje de éxito (en un caso real)
        service_vals = {
             'name': kw.get('name'),
             'child_id': int(kw.get('child')),
             'start_date': kw.get('start_date'),
             'status': kw.get('status')
         }
        print(service_vals)
        return request.redirect('/services?success=1')
    
    @http.route(['/services'], type='http', auth='user', website=True)
    def portal_services(self, **kw):
        services = [{
                "name": "After School Care 1",
                "child": "John Doe",
                "start_date": "2024-01-15",
                "status": "active"
            }, {
                "name": "Summer Camp",
                "child": "Jane Doe",
                "start_date": "2024-06-01",
                "status": "pending"
            }, {
                "name": "Weekend Activities",
                "child": "John Doe",
                "start_date": "2024-03-01",
                "status": "active"
            }]
        
        values = self._prepare_page_values('services')
        values['services'] = services
        
        # Verificar si hay mensaje de éxito
        if kw.get('success'):
            values['success_message'] = "Service created successfully!"
        
        return request.render("childcare_management.services_page", values)
    
    # Método para sobrescribir el comportamiento predeterminado de logout
    @http.route('/web/session/logout', type='http', auth="public", website=True)
    def logout_override(self, redirect='/portal/login', **kw):
        request.session.logout(keep_db=True)
        return request.redirect(redirect)