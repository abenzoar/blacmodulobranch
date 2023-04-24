# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from . import models
from odoo import api, fields, SUPERUSER_ID, _


def _uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    xml_ids = [
        'crm.crm_rule_all_lead',
        'crm.crm_rule_personal_lead',
    ]
    for xml_id in xml_ids:
        act_window = env.ref(xml_id, raise_if_not_found=False)
        if xml_id == 'crm.crm_rule_all_lead':
        	act_window.domain_force = [(1, '=', 1)]
        if xml_id == 'crm.crm_rule_personal_lead':
        	act_window.domain_force = "['|',('user_id','=',user.id),('user_id','=',False)]"


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
