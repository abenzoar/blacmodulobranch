# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from . import models
from . import report
from odoo import api, fields, SUPERUSER_ID, _


def _uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    xml_ids = [
        'helpdesk.helpdesk_ticket_user_rule',
    ]
    for xml_id in xml_ids:
        act_window = env.ref(xml_id, raise_if_not_found=False)
        if xml_id == 'helpdesk.helpdesk_ticket_user_rule':
        	act_window.domain_force = """['|', '|',
					('team_id.privacy_visibility', '!=', 'invited_internal'),
					('team_id.message_partner_ids', 'in', [user.partner_id.id]),
					('message_partner_ids', 'in', [user.partner_id.id])]"""


