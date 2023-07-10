# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    
    
    purchase_request_approver_id = fields.Boolean('Aprobar solicitudes de Compra')