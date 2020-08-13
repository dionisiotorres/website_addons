from odoo import api, fields , models
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    token_validity = fields.Integer(
    	string='Token Validity In Days',
    	help="Validity of the token in days sent in email. If validity is 0 it means infinite.",
        default=1,
	)
    restrict_unverified_users = fields.Boolean(
    	string='Restrict Unverified Users From Checkout',
    	help="If enabled unverified users can not proceed to checkout untill they verify their emails",
        default=True,
    )

    @api.model
    def check_email_is_validated(self):
        current_user = self.env['res.users'].sudo().browse(self._uid)
        status = 'verified'
        restrict_users = self.restrict_unverified_users
        if restrict_users:
            if not current_user.token_verified:
                if not current_user.signup_valid:
                    status = 'expired'
                else:
                    status = 'unverified'
        return status