# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kelvzxu (<https://kltech-intl.odoo.com/>)
# Copyright(c): 2015-kltech-intl.
# All Rights Reserved.
#################################################################################

from . import models
from . import wizard
from . import controllers

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_serie =version_info.get('server_serie')
    if server_serie!='13.0':raise Warning('Module support Odoo series 13.0 found {}.'.format(server_serie))
    return True