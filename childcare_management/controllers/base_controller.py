from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug

class BaseController(http.Controller):
    def _prepare_page_values(self, page_name=None):
        user = request.env.user
        values = {
            'page_name': page_name,
            'children_count': 3,
            'medical_records_count': 8,
            'active_services_count': 2,
            'user': user,
            'is_logged_in': not user._is_public() 
        }
        return values
    