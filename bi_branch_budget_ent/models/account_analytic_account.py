# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError



    
class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    
    branch_id = fields.Many2one('res.branch', string='Branch')


    @api.model 
    def default_get(self, field): 
        result = super(AccountAnalyticAccount, self).default_get(field)
        user_obj = self.env['res.users']
        branch_id = user_obj.browse(self.env.user.id).branch_id.id
        result['branch_id'] = branch_id
        return result

    
    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        for obj in self:
            selected_brach = obj.branch_id
            if selected_brach:
                user_id = self.env['res.users'].browse(self.env.uid)
                user_branch = user_id.sudo().branch_id
                if user_branch and user_branch.id != selected_brach.id:
                    raise UserError("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that.") 

    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
        index=True, store=True, readonly=False, check_company=True, copy=True)
    product_id = fields.Many2one('product.product', string='Product', ondelete='restrict')
    account_id = fields.Many2one('account.account', string='Account',
        index=True, ondelete="cascade",
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False)]",
        check_company=True,
        tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict')
    date = fields.Date(related='move_id.date', store=True, readonly=True, index=True, copy=False, group_operator='min')

    @api.depends('product_id', 'account_id', 'partner_id', 'date')
    def _compute_analytic_account_id(self):
        for record in self:
            if not record.exclude_from_invoice_tab or not record.move_id.is_invoice(include_receipts=True):
                rec = self.env['account.analytic.default'].account_get(
                    product_id=record.product_id.id,
                    partner_id=record.partner_id.commercial_partner_id.id or record.move_id.partner_id.commercial_partner_id.id,
                    account_id=record.account_id.id,
                    user_id=record.env.uid,
                    date=record.date,
                    company_id=record.move_id.company_id.id
                )
                if rec:
                    record.analytic_account_id = rec.analytic_id
    
        
    
