# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kelvzxu (<https://kltech-intl.odoo.com/>)
# Copyright(c): 2015-kltech-intl.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################

{
  "name"                 :  "Website Signup",
  "summary"              :  "configure signup page with dynamic fields for each website.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "author"               :  "kelvzxu",
  "website"              :  "https://kltech-intl.odoo.com",
  "description"          :  "configure signup page with dynamic fields for each website.",
  "depends"              :  ['auth_signup','website'],
  "data"                 :  ['views/auth_signup_login.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  59,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}