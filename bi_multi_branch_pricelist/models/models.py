# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime


class BiProductPricelist(models.Model):
    _inherit = "product.pricelist"

    pricelist_branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def default_get(self,fields):
        res = super(BiProductPricelist, self).default_get(fields)
        branch_id = False
        if self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'pricelist_branch_id' : branch_id
        })
        return res


class BiProductItemPricelist(models.Model):
    _inherit = "product.pricelist.item"

    branch_id = fields.Many2one('res.branch', string='Branch', readonly=True,
                                related='pricelist_id.pricelist_branch_id', store=True)
