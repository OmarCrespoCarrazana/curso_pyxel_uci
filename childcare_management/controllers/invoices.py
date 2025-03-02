from odoo import http
from odoo.http import request
from .base_controller import BaseController

class InvoicesController(BaseController):
    @http.route('/invoices', type='http', auth="public", website=True)
    def portal_invoices(self, redirect=None, **kw):
        invoices = [
                    {
                        'number': 'INV-2024-001',
                        'date': '2024-01-15',
                        'child': 'John Doe',
                        'service': 'After School Care',
                        'amount': '$150.00',
                        'status': 'Paid'
                    },
                    {
                        'number': 'INV-2024-002',
                        'date': '2024-02-01',
                        'child': 'Jane Doe',
                        'service': 'Summer Camp',
                        'amount': '$250.00',
                        'status': 'Pending'
                    },
                    {
                        'number': 'INV-2024-003',
                        'date': '2024-02-15',
                        'child': 'John Doe',
                        'service': 'Weekend Activities',
                        'amount': '$75.00',
                        'status': 'Overdue'
                    }
        ]
        
        values = self._prepare_page_values('invoices')
        values['invoices'] = invoices
        
        return request.render('childcare_management.invoices_page', values)
