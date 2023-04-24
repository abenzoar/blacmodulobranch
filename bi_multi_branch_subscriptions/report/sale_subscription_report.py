# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID, tools

class SaleSubscriptionReport(models.Model):
    _inherit = 'sale.subscription.report'

    branch_id = fields.Many2one('res.branch', 'Branch', readonly=True)

    def _select(self):
        select_str = super()._select()
        select_str += ", sub.branch_id as branch_id"
        return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", sub.branch_id"
        return group_by_str