# -*- coding: utf-8 -*-
# from odoo import http


# class ChildcareManagement(http.Controller):
#     @http.route('/childcare_management/childcare_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/childcare_management/childcare_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('childcare_management.listing', {
#             'root': '/childcare_management/childcare_management',
#             'objects': http.request.env['childcare_management.childcare_management'].search([]),
#         })

#     @http.route('/childcare_management/childcare_management/objects/<model("childcare_management.childcare_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('childcare_management.object', {
#             'object': obj
#         })

