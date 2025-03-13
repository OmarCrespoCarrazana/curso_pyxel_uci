# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
from .base_controller import BaseController
import logging
_logger = logging.getLogger(__name__)

class Logout(BaseController):
    
    @http.route('/logout', type='http', auth="user", website=True)
    def logout(self):
        request.session.logout()
        return request.redirect('/')    
    # Método para sobrescribir el comportamiento predeterminado de logout
    @http.route('/web/session/logout', type='http', auth="public", website=True)
    def logout_override(self, redirect='/portal/login', **kw):
        request.session.logout(keep_db=True)
        return request.redirect(redirect)