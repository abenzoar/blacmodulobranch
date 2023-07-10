from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_purchase_request = fields.Boolean(string='Se puede solicitar')