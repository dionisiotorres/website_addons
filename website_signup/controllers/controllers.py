# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteSignup(http.Controller):
#     @http.route('/website_signup/website_signup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_signup/website_signup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_signup.listing', {
#             'root': '/website_signup/website_signup',
#             'objects': http.request.env['website_signup.website_signup'].search([]),
#         })

#     @http.route('/website_signup/website_signup/objects/<model("website_signup.website_signup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_signup.object', {
#             'object': obj
#         })
