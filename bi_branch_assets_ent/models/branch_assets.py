# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, tools


class AccountsAsset(models.Model):
    _inherit = "account.asset"

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def default_get(self, field):
        result = super(AccountsAsset, self).default_get(field)
        user_obj = self.env['res.users']
        branch_id = user_obj.browse(self.env.user.id).branch_id.id
        result['branch_id'] = branch_id
        return result

    def validate(self):
        res = super(AccountsAsset, self).validate()
        self.depreciation_move_ids.write({'branch_id': self.branch_id.id})
        for move_line in self.depreciation_move_ids.line_ids:
            move_line.write({'branch_id': self.branch_id.id})
        return res
