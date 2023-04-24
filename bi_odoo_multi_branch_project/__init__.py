# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from . import models
from . import report
from odoo import api, fields, SUPERUSER_ID, _


def _uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    xml_ids = [
        'project.project_project_manager_rule',
        'project.project_public_members_rule',
        'project.project_manager_all_project_tasks_rule',
        'project.task_visibility_rule'
    ]
    for xml_id in xml_ids:
        act_window = env.ref(xml_id, raise_if_not_found=False)
        if xml_id == 'project.project_project_manager_rule':
        	act_window.domain_force = [(1, '=', 1)]
        if xml_id == 'project.project_public_members_rule':
        	act_window.domain_force = "['|',('privacy_visibility', '!=', 'followers'),('message_partner_ids', 'in', [user.partner_id.id])]"
        if xml_id == 'project.project_manager_all_project_tasks_rule':
        	act_window.domain_force = [(1,'=',1)]
        if xml_id == 'project.task_visibility_rule':
        	act_window.domain_force = "['|',('project_id.privacy_visibility', '!=', 'followers'),'|',('project_id.message_partner_ids', 'in', [user.partner_id.id]),'|',('message_partner_ids', 'in', [user.partner_id.id]),('user_ids', 'in', user.id)]"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
