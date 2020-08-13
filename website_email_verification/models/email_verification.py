from odoo import api, fields, models, _
from odoo.addons.auth_signup.models.res_partner import now
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users' 

    token_verified = fields.Boolean(
        string='Token Verified', default=True)

    @api.model
    def send_verification_email(self, res_id):
        user = self.browse(res_id)
        validity = self.env['website'].get_current_website().token_validity
        expiration = now(days=+validity)
        temp_id = self.env.ref('website_email_verification.odoo_email_verification_email_template_id')
        user.partner_id.signup_prepare(signup_type="verify", expiration=expiration)
        if temp_id:
            try:
                res = temp_id.send_mail(res_id, True)
            except Exception as e:
                return False
        return True

    @api.model
    def create(self, vals):
        vals['token_verified'] = False
        res_id = super(ResUsers, self).create(vals)
        self.send_verification_email(res_id.id)
        return res_id

    @api.model
    def get_verification_url(self):
        db =self._cr.dbname
        if self.signup_token and db:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = '/web/login'
            url = "%s/web/email/verification?db=%s&verify_token=%s&verify_uid=%s"%(base_url, db,self.signup_token,self.id)
            return url
        return False

    @api.model
    def verify_email(self, params={}):
        status = 'error'
        msg = "Oops!!. There is some error currently please try after some time."
        try:
            if params.get('verify_token') and params.get('verify_uid') and params.get('db'):
                uid = int(params.get('verify_uid'))
                token = str(params.get('verify_token'))
                user = request.env['res.users'].sudo().browse(uid)
                msg = "Your account has been verified. You will be automatically redirected to Home page."
                if not user.token_verified:
                    if user.signup_token == token:
                        if not user.signup_valid:
                            status = 'expired'
                            msg = "This link has been expired. Resend a new verification link from your account."
                        else:
                            user.token_verified = True
                            status = 'verified'
                    else:
                        status = 'unverified'
                        msg = "The account is not verified yet. Resend a new verification link from your account."
                else:
                    status = 'already_verified'
                    msg = "Your account has already been verified. You will be automatically redirected to Home page."
        except Exception as e:
            status = 'error'
            msg = "Oops!!. There is some error currently please try after some time."
        return {'status':status,'msg':msg}

    def resend_verification_user_email(self):
        msg =  "A new email has been sent to this user successfully."
        res = self.send_verification_email(self.id)
        if not res:
            msg = 'Exception in sending the email. Please try again later.'
        wizard_id = self.env['wizard.message'].create(
                {'text': msg})
        return {'name': _("Summary"),
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'wizard.message',
                'res_id': wizard_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                }


    def verify_email_manually(self):
        self.token_verified = True
        wizard_id = self.env['wizard.message'].create(
                {'text': "Email has been verified manually!!"})
        return {'name': _("Summary"),
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'wizard.message',
                'res_id': wizard_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                }