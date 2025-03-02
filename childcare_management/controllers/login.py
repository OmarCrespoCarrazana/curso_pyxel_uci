from odoo import http
from odoo.http import request

class AuthController(http.Controller):
    @http.route('/portal/login', type='http', auth="public", website=True, sitemap=False)
    def login(self, redirect=None, **kw):
        if request.session.uid:
            return request.redirect('/')
            
        values = {
            'error': request.params.get('error', ''),
            'redirect': redirect,
        }
        
        if request.httprequest.method == 'POST':
            try:
                uid = request.session.authenticate(
                    request.session.db, 
                    request.params['login'], 
                    request.params['password']
                )
                if uid:
                    user = request.env.user
                    if user.has_group('base.group_user'):
                        return request.redirect('/web')
                    return request.redirect('/')
                values['error'] = 'Invalid credentials'
            except Exception as e:
                values['error'] = str(e)

        
        return request.render('childcare_management.custom_login', values)

    @http.route('/logout', type='http', auth="user", website=True)
    def logout(self):
        request.session.logout()
        return request.redirect('/portal/login')