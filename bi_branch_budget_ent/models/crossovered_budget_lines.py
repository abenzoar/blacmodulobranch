# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError



    
class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"
    _description = "Budget Line"


    @api.model 
    def default_get(self, field): 
        result = super(CrossoveredBudgetLines, self).default_get(field)
        user_obj = self.env['res.users']
        branch_id = user_obj.browse(self.env.user.id).branch_id.id
        result['branch_id'] = branch_id
        return result
    

    branch_id = fields.Many2one( 'res.branch', related='crossovered_budget_id.branch_id', string='Branch', store=True)
    
    
    
    def action_open_budget_entries(self):
        if self.crossovered_budget_id.branch_id:
            if self.analytic_account_id:
                # if there is an analytic account, then the analytic items are loaded
                action = self.env['ir.actions.act_window']._for_xml_id('analytic.account_analytic_line_action_entries')
                action['domain'] = [('account_id', '=', self.analytic_account_id.id),
                                    ('date', '>=', self.date_from),
                                    ('date', '<=', self.date_to),
                                    ('branch_id', '=', self.crossovered_budget_id.branch_id.id),
                                    ]
                if self.general_budget_id:
                    action['domain'] += [('general_account_id', 'in', self.general_budget_id.account_ids.ids)]
            else:
                # otherwise the journal entries booked on the accounts of the budgetary postition are opened
                action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_moves_all_a')
                action['domain'] = [('account_id', 'in',
                                     self.general_budget_id.account_ids.ids),
                                    ('date', '>=', self.date_from),
                                    ('date', '<=', self.date_to),
                                    ('branch_id', '=', self.crossovered_budget_id.branch_id.id),
                                    ]
        else:
            if self.analytic_account_id:
                # if there is an analytic account, then the analytic items are loaded
                action = self.env['ir.actions.act_window']._for_xml_id('analytic.account_analytic_line_action_entries')
                action['domain'] = [('account_id', '=', self.analytic_account_id.id),
                                    ('date', '>=', self.date_from),
                                    ('date', '<=', self.date_to)
                                    ]
                if self.general_budget_id:
                    action['domain'] += [('general_account_id', 'in', self.general_budget_id.account_ids.ids)]
            else:
                # otherwise the journal entries booked on the accounts of the budgetary postition are opened
                action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_moves_all_a')
                action['domain'] = [('account_id', 'in',
                                     self.general_budget_id.account_ids.ids),
                                    ('date', '>=', self.date_from),
                                    ('date', '<=', self.date_to)
                                    ]
        return action
    
    
    
    
    def _compute_practical_amount(self):
        for line in self:
            if line.crossovered_budget_id.branch_id:
                acc_ids = line.general_budget_id.account_ids.ids
                date_to = line.date_to
                date_from = line.date_from
                if line.analytic_account_id.id:
                    analytic_line_obj = self.env['account.analytic.line']
                    domain = [('account_id', '=', line.analytic_account_id.id),
                              ('date', '>=', date_from),
                              ('date', '<=', date_to),
                              ('branch_id', '=', line.crossovered_budget_id.branch_id.id),
                              ]
                    if acc_ids:
                        domain += [('general_account_id', 'in', acc_ids)]
    
                    where_query = analytic_line_obj._where_calc(domain)
                    analytic_line_obj._apply_ir_rules(where_query, 'read')
                    from_clause, where_clause, where_clause_params = where_query.get_sql()
                    select = "SELECT SUM(amount) from " + from_clause + " where " + where_clause
    
                else:
                    aml_obj = self.env['account.move.line']
                    domain = [('account_id', 'in',
                               line.general_budget_id.account_ids.ids),
                              ('date', '>=', date_from),
                              ('date', '<=', date_to),
                              ('move_id.state', '=', 'posted'),
                              ('branch_id', '=', line.crossovered_budget_id.branch_id.id),
                              ]
                    where_query = aml_obj._where_calc(domain)
                    aml_obj._apply_ir_rules(where_query, 'read')
                    from_clause, where_clause, where_clause_params = where_query.get_sql()
                    select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause
    
                self.env.cr.execute(select, where_clause_params)
                line.practical_amount = self.env.cr.fetchone()[0] or 0.0
            else:
                acc_ids = line.general_budget_id.account_ids.ids
                date_to = line.date_to
                date_from = line.date_from
                if line.analytic_account_id.id:
                    analytic_line_obj = self.env['account.analytic.line']
                    domain = [('account_id', '=', line.analytic_account_id.id),
                              ('date', '>=', date_from),
                              ('date', '<=', date_to),
                              ]
                    if acc_ids:
                        domain += [('general_account_id', 'in', acc_ids)]
    
                    where_query = analytic_line_obj._where_calc(domain)
                    analytic_line_obj._apply_ir_rules(where_query, 'read')
                    from_clause, where_clause, where_clause_params = where_query.get_sql()
                    select = "SELECT SUM(amount) from " + from_clause + " where " + where_clause
    
                else:
                    aml_obj = self.env['account.move.line']
                    domain = [('account_id', 'in',
                               line.general_budget_id.account_ids.ids),
                              ('date', '>=', date_from),
                              ('date', '<=', date_to),
                              ('move_id.state', '=', 'posted')
                              ]
                    where_query = aml_obj._where_calc(domain)
                    aml_obj._apply_ir_rules(where_query, 'read')
                    from_clause, where_clause, where_clause_params = where_query.get_sql()
                    select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause
    
                self.env.cr.execute(select, where_clause_params)
                line.practical_amount = self.env.cr.fetchone()[0] or 0.0

                    
                
            
            
