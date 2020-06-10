# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kelvzxu (<https://kltech-intl.odoo.com/>)
# Copyright(c): 2015-kltech-intl.
# All Rights Reserved.
#################################################################################

{
  "name"                 :  "Website Signup",
  "summary"              :  "configure signup page with dynamic fields for each website.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "author"               :  "kelvzxu",
  "website"              :  "https://kltech-intl.odoo.com",
  "description"          :  "configure signup page with dynamic fields for each website.",
  "depends"              :  ['auth_signup','website',],
  "data"                 :  [
                              "security/ir.model.access.csv",
                              "views/website_signup_views.xml",
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  59,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}