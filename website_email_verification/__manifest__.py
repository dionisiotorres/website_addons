# -*- coding: utf-8 -*-
{
    'name': "website_email_verification",
    "summary"              :  "This module allows to send token based email for verification of accounts and restricts checkout for non verified accounts.",
    "category"             :  "Website",
    "version"              :  "3.0.1",
    "sequence"             :  10,
    "author"               :  "kelvzxu",
    "website"              :  "https://kltech-intl.odoo.com",
    "live_test_url"        :  "",
    "depends"              :  [
                                'mail',
                                'website',
                                'website_sale',
                                ],
    "data"                 :  [
                                'data/email_template.xml',
                                'views/templates_view.xml',
                                'views/res_users_view.xml',
                                'wizard/wizard_view.xml',
                                ],
    "images"               :  ['static/description/banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  25,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",
}