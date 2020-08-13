import logging
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import werkzeug.utils
from odoo.addons.web.controllers.main import  Home
_logger = logging.getLogger(__name__)
class Home(Home):

    @http.route('/web/email/verification', type='http', auth="none")
    def web_email_verification(self, redirect=None, **kw):
        res = request.env['res.users'].verify_email(kw)
        return request.render('website_email_verification.email_verification_template',{'status':res['status'],'msg':res['msg']})

    @http.route('/resend/email', type='http', auth='public', website=True)
    def resend_email(self, *args, **kw):
        user = request.env['res.users']
        user_id = user.browse([request.uid])
        post_params = ''
        if not user_id.token_verified:
            user.sudo().send_verification_email(request.uid)
        else:
            href = request.httprequest.referrer
            if '#' in href:
                href = href + '&is_verified=True'
            else:
                href = href + '#is_verified=True'
            return request.redirect(href)
        return
