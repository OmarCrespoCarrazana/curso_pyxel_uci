from odoo import http
from odoo.http import request
from .base_controller import BaseController
import logging
_logger = logging.getLogger(__name__)

class InvoicesController(BaseController):
    @http.route('/invoices', type='http', auth="public", website=True)
    def portal_invoices(self, redirect=None, **kw):
        values = self._prepare_page_values('invoices')    
        return request.render('childcare_management.invoices_page', values)
