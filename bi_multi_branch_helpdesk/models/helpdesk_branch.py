# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def default_get(self, default_fields):
        res = super(HelpdeskTicket, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id': branch_id
        })
        return res


