# -*- coding: utf-8 -*-
from odoo import models, fields, api


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    hfoc_supplier_id = fields.Many2one('res.partner')


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    hfoc_supplier_bool = fields.Boolean(string="Proveedor por default para solicitudes de compra - SERVICIO")
    hfoc_supplier_id = fields.Many2one('res.partner',  related='company_id.hfoc_supplier_id', readonly=False, string='Proveedor por default')
    hfoc_request_block = fields.Boolean(string="No permitir solicitudes de compra si el producto no cuenta con proveedor") 
    

    def set_values(self):
        res=super(ResConfigSetting, self).set_values()
        self.env['ir.config_parameter'].set_param('hfoc_supplier_bool', self.hfoc_supplier_bool)
        self.env['ir.config_parameter'].set_param('hfoc_num', self.hfoc_request_block)

        return res
    
    
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        hfoc_supplier_bool = self.env['ir.config_parameter'].sudo().get_param('hfoc_supplier_bool')
        hfoc_request_block = self.env['ir.config_parameter'].sudo().get_param('hfoc_request_block')

        
        res.update(
            hfoc_supplier_bool=hfoc_supplier_bool,
            hfoc_request_block=hfoc_request_block,
        )
        return res