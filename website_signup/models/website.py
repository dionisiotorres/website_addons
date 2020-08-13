from odoo import models
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    def get_active_website_setting(self):
        website_id = self.env['website'].get_current_website()
        if website_id:
            active_rec = self.env['web.signup.settings'].sudo().search([
                ('website_id', '=', website_id.id), ('active', '=', True)
                ], limit=1)
            return active_rec
        return False

    def get_all_field_values(self, field_id):
        f_values = {}
        field = self.env['web.signup.fields'].browse(int(field_id))
        domain = field.field_domain or []
        obj_rel = field.sudo().get_field_obj_relation()
        if domain:
            domain = safe_eval(domain)
        objs = self.env[obj_rel].sudo().search(domain)
        if objs:
            for rec in objs:
                field_type = field.sudo().field
                if field_type.name.startswith('property_'):
                    f_values[field_type.relation + ',' + str(rec.id)] = rec.name
                else:
                    f_values[rec.id] = rec.name
        return f_values

    def get_signup_fields(self):
        signup_obj = self.get_active_website_setting()
        signup_field_list = []
        if signup_obj:
            if signup_obj.signup_field_ids:
                for field in signup_obj.signup_field_ids:
                    field_dict = {}
                    f_name = field.field.name
                    f_input_type = field.field_input_type
                    field_dict[f_name] = {
                        'input_type': field.field_input_type,
                        'placeholder': field.placeholder or '',
                        'title': field.help or '',
                        'label': field.field_label or field.field.field_description or '',
                        'is_required': field.is_required,
                        'cols': int(field.no_of_cols),
                    }
                    if f_input_type == 'selection':
                        f_values = dict(request.env['res.partner']._fields[f_name].selection)
                        field_dict[f_name].update({'f_values': f_values})
                    if f_input_type in ['selection_m2o', 'selection_m2m']:
                        f_values = self.get_all_field_values(field.id)
                        field_dict[f_name].update({'f_values': f_values})
                    signup_field_list.append(field_dict)
        return signup_field_list

    def is_login_signup_page(self):
        path = request.httprequest.full_path
        if path.find("/web/login") == 0 or path.find("/web/signup") == 0 or path.find("/web/reset_password") == 0:
            return True
        return False

    def is_signup_page(self):
        if request.httprequest.full_path.find('/web/signup') == 0:
            return True
        return False
