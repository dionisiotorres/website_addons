# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kelvzxu (<https://kltech-intl.odoo.com/>)
# Copyright(c): 2015-kltech-intl.
# All Rights Reserved.
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError

SIGNUP_FIELD_TYPES = [
    'char',
    'integer',
    'float',
    'boolean',
    'text',
    'selection',
    'many2one',
    'many2many',
]
FIELDS_INPUT_TYPE = [
    ('char', 'text'),
    ('integer', 'number'),
    ('float', 'float'),
    ('boolean', 'checkbox'),
    ('text', 'textarea'),
    ('selection', 'selection'),
    ('many2one', 'selection_m2o'),
    ('many2many', 'selection_m2m'),
]

class WebsiteSignupSettings(models.Model):
    _name = "web.signup.settings"
    _order = "active desc"

    @api.model
    def get_active_website_setting(self, website_id):
        active_rec = self.search([('website_id','=',int(website_id)),('active','=',True)], limit=1)
        return active_rec

    def _default_website(self):
        return self.env['website'].search([
            ('company_id', '=', self.env.user.company_id.id)],
            limit=1,
        )

    website_id = fields.Many2one('website',
        string= "Website",
        default= _default_website,
        ondelete= 'cascade',
        required= True,
        )
    name= fields.Char("Name", required=True, translate=True)
    active = fields.Boolean('Active', default=False)
    hide_header = fields.Boolean("Hide header from Signup Page",
        copy= True,
        )
    hide_footer = fields.Boolean("Hide footer from Signup Page",
        copy= True,
        )
    show_t_n_c = fields.Boolean("Show Terms and Condition in Signup Page",
        copy= True,
        )
    background_type = fields.Selection([
        # ('color','Color'),
        ('image','Image'),
        ('none','None'),
        ], string= "Background Type",
        default= "none",
        copy= True,
        readonly= False,
        )
    bg_img = fields.Binary("Background Image",
        copy=True,
        readonly=False,
        )
    signup_page_content = fields.Html("SignUp Page Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic; \
         font-variant-ligatures: initial; font-variant-caps: initial; font-weight: initial;\
         text-align: inherit;">Registration is free and easy! Please enter the following \
         information to create your account.</span></p>'
        )
    login_page_content = fields.Html("Login Page Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic;">If you have an\
         account with us, please log in.</span></p>'
        )
    reset_passw_page_content = fields.Html("Reset Password Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic;">Please \
         enter your email address below. You will receive a link to reset your password.</span></p>'
        )
    t_n_c_content = fields.Html("Terms and Condition",
        copy=True,
        translate=True,
        default="<p> Terms and Condition <p>"
        )
    signup_field_ids = fields.One2many("web.signup.fields",
        "website_signup_setting_id",
        "SignUp Fields",
        )

    def toggle_active(self):
        if self.active:
            raise UserError(_("You have already set this settings as active."))
        active_website_setting = self.search(
            [('active', '=', True),('website_id', 'in', [self.website_id.id])])
        if active_website_setting:
            active_website_setting.write({'active': False})
        self.active = True
        return

    @api.model
    def create(self, vals):
        if vals.get("website_id"):
            active_website_setting = self.search(
                [('active', '=', True),('website_id', 'in', [int(vals.get("website_id"))])])
            if not active_website_setting:
                vals.update({'active':True,})
        res = super(WebsiteSignupSettings, self).create(vals)
        return res

class WebsiteSignupFields(models.Model):
    _name = "web.signup.fields"
    _order = "sequence"

    @api.depends("field_type")
    def _compute_field_input_type(self):
        for rec in self:
            field_type = rec.field_type
            if field_type:
                input_type = [item for item in FIELDS_INPUT_TYPE if field_type in item[0]]
                if input_type and input_type[0] and input_type[0][1]:
                    rec.field_input_type = input_type[0][1]

    field = fields.Many2one("ir.model.fields", "Signup Field", size=32,
        required=True, help="Associated field in the SignUp form.",
        domain="[('model', 'in', ['res.partner']),('ttype', 'in', %s),('name','not in',['email','name'])]" % SIGNUP_FIELD_TYPES,
    )
    field_type = fields.Selection("Field Type",
            related = "field.ttype",
            store = True,
            help="Associated field type in the SignUp form.",)
    field_domain = fields.Char("Field Domain")
    field_input_type = fields.Char("Input Type", help="Field input type in signup form",
        compute = "_compute_field_input_type", store=True)
    no_of_cols = fields.Selection([('1','1'),('2','2')], "Number of columns",
        help="Number of columns in signup form")
    is_required = fields.Boolean("Is required",
        help="Enable if associated field will be required")
    sequence = fields.Integer("Sequence",
        help="Sequence number for this field in signup form")
    field_label = fields.Char("Field Label",
        help="Label for this field in signup form",
        translate=True)
    placeholder = fields.Char("Placeholder",
        help="Placeholder value for this field in signup form",
        translate=True)
    help = fields.Text("Help",
        help="Description for this field to customers in signup form",
        translate=True)
    website_signup_setting_id = fields.Many2one("web.signup.settings", "Signup Settings")

    @api.onchange("field")
    def _compute_field_label(self):
        for rec in self:
            if rec.field:
                rec.field_label = rec.field.field_description
                rec.field_domain = ''

    def get_field_obj_relation(self):
        for rec in self:
            obj_relation = None
            field = rec.field
            if field and rec.field_type in ['many2one', 'many2many']:
                obj_relation = field.relation
        return obj_relation

    def action_add_domain(self):
        obj_relation = self.get_field_obj_relation()
        view_id = self.env["field.add.domain"].create({})
        vals = {
            'name' : _("Add Domain"),
            'view_mode' : 'form',
            # 'view_type' : 'form',
            'res_model' : 'field.add.domain',
            'res_id' : view_id.id,
            'context' : "{'obj_relation': '%s'}" % obj_relation,
            'type' : "ir.actions.act_window",
            'target' : 'new',
         }
        return vals
