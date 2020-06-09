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
  "name"                 :  "Website Show Password",
  "summary"              :  "view password at login and signup page",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "author"               :  "kelvzxu",
  "website"              : "https://kltech-intl.odoo.com",
  "description"          :  "view password at login and signup page",
  "depends"              :  ['website'],
  "data"                 :  ['views/auth_signup_login.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "pre_init_hook"        :  "pre_init_check",
}