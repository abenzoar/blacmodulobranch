# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID, tools


class HelpDeskReport(models.Model):
    _inherit = "helpdesk.ticket.report.analysis"

    branch_id = fields.Many2one('res.branch', string='Branch')

    def _select(self):
        return super(HelpDeskReport, self)._select() + """, T.branch_id AS branch_id"""

    def _group_by(self):
        return super(HelpDeskReport, self)._group_by() + """, sub.branch_id"""


