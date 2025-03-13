# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
from .base_controller import BaseController
import logging

_logger = logging.getLogger(__name__)

class AccountController(BaseController):
    @http.route(['/account', '/my/account'], type='http', auth='user', website=True)
    def account_profile(self, **kw):
        values = self._prepare_page_values('profile', **kw)
        return request.render("childcare_management.portal_account_custom", values)
    
    @http.route(['/account/security', '/my/security'], type='http', auth='user', website=True)
    def account_security(self, **kw):
        values = self._prepare_page_values('security', **kw)
        return request.render("childcare_management.portal_account_custom", values)
    
    @http.route(['/account/get_user_data'], type='json', auth='user', website=True)
    def get_user_data(self, **kw):
        """Endpoint para obtener los datos del usuario para el componente OWL"""
        user = request.env.user
        
        try:
            data = {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'street': user.street,
                'street2': user.street2,
                'city': user.city,
                'zip': user.zip,
                'country_id': user.country_id.id if user.country_id else False,
                'state_id': user.state_id.id if user.state_id else False,
            }
            return data
            
        except Exception as e:
            _logger.error("Error getting user data: %s", str(e))
            return {'error': str(e)}
    
    @http.route(['/account/update_profile_json'], type='json', auth='user', website=True)
    def update_profile_json(self, **kw):
        """Endpoint para actualizar el perfil del usuario desde el componente OWL"""
        user = request.env.user
        
        try:
            # Update user information
            vals = {
                'name': kw.get('name'),
                'email': kw.get('email'),
                'phone': kw.get('phone'),
                'street': kw.get('street'),
                'street2': kw.get('street2'),
                'city': kw.get('city'),
                'zip': kw.get('zip'),
            }
            
            # Only update state and country if provided
            if kw.get('country_id'):
                vals['country_id'] = int(kw.get('country_id'))
            if kw.get('state_id'):
                vals['state_id'] = int(kw.get('state_id'))
                
            user.sudo().write(vals)
            _logger.info("User %s updated their profile information", user.id)
            
            return {'success': True, 'message': 'Profile updated successfully'}
            
        except Exception as e:
            _logger.error("Error updating user profile via JSON: %s", str(e))
            return {'success': False, 'error': str(e)}
    
    @http.route(['/account/change_password_json'], type='json', auth='user', website=True)
    def change_password_json(self, **kw):
        """Endpoint para cambiar la contraseña del usuario desde el componente OWL"""
        user = request.env.user
        
        try:
            current_password = kw.get('current_password')
            new_password = kw.get('new_password')
            confirm_password = kw.get('confirm_password')
            
            # Validate passwords
            if not current_password or not new_password or not confirm_password:
                return {'success': False, 'error': 'All fields are required'}
                
            if new_password != confirm_password:
                return {'success': False, 'error': 'New passwords do not match'}
                
            if len(new_password) < 8:
                return {'success': False, 'error': 'Password must be at least 8 characters long'}
            
            # Check current password
            try:
                request.env['res.users'].change_password(current_password, new_password)
                new_token = request.env.user._compute_session_token(request.session.sid)
                request.session.session_token = new_token
            except:
                return {'success': False, 'error': 'Current password is incorrect'}
           
            _logger.info("User %s changed their password via JSON", user.id)
            
            return {'success': True, 'message': 'Password changed successfully','session_token': new_token}
            
        except Exception as e:
            _logger.error("Error updating password via JSON: %s", str(e))
            return {'success': False, 'error': str(e)}