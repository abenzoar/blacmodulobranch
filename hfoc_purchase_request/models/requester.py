# -*- coding: utf-8 -*-
from odoo import api, fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_STATES = [
    ('rejected', 'Rechazado'),
    ('draft', 'Borrador'),
    ('to_rectify', 'Por rectificar'),
    ('to_process', 'Por aprobar'),
    ('approve', 'Aprobado'),   
]


_PAYMENT = [
    ('payment_draft', 'Solicitado'),
]


class PurchaserequesterLine(models.Model):
    _name = "purchase.requester.line"
    _description = "Lineas de solicitudes de compra"

    name = fields.Text('Descripción', track_visibility='onchange')
    product_id = fields.Many2one('product.product', 'Producto', domain=[('purchase_ok', '=', True),('is_purchase_request','=',True)], required=True, track_visibility='onchange')
    product_uom_id = fields.Many2one('product.uom', 'Unid. Medida', track_visibility='onchange')
    product_qty = fields.Float(string='Cantidad', track_visibility='onchange', digits=dp.get_precision('Unidad de medida del producto'))
    request_id = fields.Many2one('purchase.requester','Solicitud de compra', ondelete='cascade', readonly=True)
    company_id = fields.Many2one('res.company', related="request_id.company_id", string='Compañia', store=True )
    state = fields.Selection(string='Estado', selection=_STATES, default="draft")
    supplier_id = fields.Many2one('res.partner',string='Proveedor', compute="_compute_supplier_id")
    is_editable = fields.Boolean(string='Es editable', readonly=True)
    detailed_type = fields.Selection([('consu','Consumible'),
                                      ('product','Almacenable'),
                                      ('service','Servicio')], related="product_id.detailed_type", string='Tipo de producto')
    purchase_order_line_id = fields.Many2one('purchase.order.line', string='Linea de orden de compra')
    payment_state = fields.Selection(string='Pago', selection=_PAYMENT)
    
    def unlink(self):
        for self in self:
            if self.purchase_order_line_id.order_id == 'draft':
                self.purchase_order_line_id.unlink()

        return super(PurchaserequesterLine, self).unlink()
    
    def send_message(self,msn):
        user_ids=[]
        user_ids.append(self.request_id.requested_by.partner_id.id)
        user_ids.append(self.request_id.approver_id.partner_id.id)
        mail_channel= self.env['mail.channel'].search([('active','=',True)])
        channel_id = False
        for line in mail_channel:
            if len(line.channel_member_ids) == 2:
                partner_ids = line.channel_member_ids.mapped('partner_id').ids
                if partner_ids == user_ids:
                    channel_id = line.id
                    break
        if channel_id == False:            
            new_channel = self.env['mail.channel'].create({
                'name': '%s, %s' % (self.request_id.requested_by.partner_id.name,self.request_id.approver_id.partner_id.name),
                'channel_type':'chat',
                'is_chat':True
             })            
            self.env['mail.channel.member'].create({
                'partner_id':self.request_id.approver_id.partner_id.id,
                'channel_id':new_channel.id
            })
            channel_id = new_channel.id
        mensage = ''
        if msn == 'payment':
            mensage = """<div style="color:#5132b9; font-size:14px" ><br/><b>"%s"</b> ha solicitado el pago para el servicio <b>"%s"</b>, documento de origen <b>"%s"</b>.
                        <br/></div>""" % (self.request_id.requested_by.name,self.product_id.display_name,self.request_id.name)

        
            channel = self.env['mail.channel'].browse(channel_id)
            channel.sudo().message_post(body=mensage, author_id=self.env.user.partner_id.id)
    
    def payment_request(self):
        self.payment_state = 'payment_draft'
        self.send_message('payment')

        

    def apply_state_to_process(self):        
        hfoc_supplier_bool = self.env['res.config.settings'].sudo().get_values().get("hfoc_supplier_bool")
        hfoc_supplier_id = self.env.company.hfoc_supplier_id

        if hfoc_supplier_bool == False or not hfoc_supplier_id:
            if self.product_id.detailed_type == 'service':
                raise UserError('El proveedor por default del SERVICIO no esta configurado.')

        if not self.product_id.seller_ids and self.product_id.detailed_type != 'service':
            raise UserError('El producto "%s" no tiene un proveedor configurado.' % self.product_id.display_name)        
        
        order_line = [(0, 0,{'product_id' : self.product_id.id,
                        'product_uom' : self.product_id.uom_po_id.id,
                        'date_planned' :  datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                        'taxes_id' : self.product_id.taxes_id.ids,
                        'product_qty' : self.product_qty,
                        'name' : self.name,
                        'purchase_requester_line_id': self.id
                        })]
        
        if not self.purchase_order_line_id:
            for line in self.request_id.purchase_order_id:
                if line.partner_id == self.supplier_id and self.product_id.detailed_type != 'service':
                    order_line[0][2]['order_id'] = line.id
                    self.purchase_order_line_id = self.env['purchase.order.line'].sudo().create(order_line[0][2])
                    self.state = 'to_process'
                if line.partner_id == hfoc_supplier_id and self.product_id.detailed_type == 'service':
                    order_line[0][2]['order_id'] = line.id
                    self.purchase_order_line_id = self.env['purchase.order.line'].sudo().create(order_line[0][2])
                    self.state = 'to_process'

            suppliers = self.request_id.purchase_order_id.mapped('partner_id')
            # raise UserError(str('%s  %s  %s ' %  (self.supplier_id.id, suppliers.ids , hfoc_supplier_id.id) ))
            supplier_id = self.supplier_id
            if self.product_id.detailed_type == 'service':
                supplier_id = hfoc_supplier_id

            if supplier_id not in suppliers:
                #raise UserError(str(suppliers))
                purchase_order = {
                    'partner_id': supplier_id.id ,
                    'company_id': self.company_id.id,
                    'user_id': self.request_id.approver_id.id,
                    'purchase_requester_id': self.request_id.id,
                    'currency_id': self.supplier_id.property_purchase_currency_id.id or self.env.user.company_id.currency_id.id,
                    'payment_term_id': self.supplier_id.property_supplier_payment_term_id.id,
                    'date_order': self.request_id.date_order,
                    'pr_note': self.request_id.note
                }

                purchase = self.env['purchase.order'].sudo().create(purchase_order)
                order_line[0][2]['order_id'] = purchase.id
                self.purchase_order_line_id = self.env['purchase.order.line'].sudo().create(order_line[0][2])
                self.state = 'to_process'
        else:
            self.purchase_order_line_id.sudo().write(order_line[0][2])
            self.state = 'to_process'
        
        


    @api.depends('product_id')
    def _compute_supplier_id(self):
        for self in self:
            if self.product_id.seller_ids:
                self.supplier_id = self.product_id.seller_ids[0].id
            else:
                self.supplier_id = False

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = '[%s] %s' % (self.product_id.code,name)
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.name = name
    

class Purchaserequester(models.Model):
    _name = "purchase.requester"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Solicitud de compra'
    _order = 'id desc'
    _rec_name = 'name'

    name = fields.Char(string="Referencia", required=True, copy=False,  index=True, default=lambda self: 'Nuevo')
    is_editable = fields.Boolean(string="Es editable", compute="_compute_is_editable", readonly=True)
    requested_by = fields.Many2one('res.users', 'Solicitado por', required=True, track_visibility='onchange', default=lambda self: self.env.user.id)
    approver_id = fields.Many2one('res.users', string='Aprobado por', required=True, track_visibility='always')    
    note = fields.Text(string="Notas", track_visibility='always')
    date_order = fields.Datetime('Fecha de solicitud', required=True, index=True, copy=False, default=datetime.today(), readonly=False, track_visibility='always')
    purchase_order_id = fields.One2many('purchase.order', 'purchase_requester_id', string='Compra')
    state = fields.Selection(_STATES, string='Estado', default='draft', compute="_compute_state", store=True, readonly=True, track_visibility='always')
    line_ids = fields.One2many('purchase.requester.line', 'request_id', 'Productos a solicitar', track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Compañia', store=True , default=lambda self:self.env.company.id)
    
    def unlink(self):
        for self in self:
            if self.purchase_order_id:
                raise UserError('No se puede eliminar, intente convertir en borrador todas las lineas de solicitud.')

        return super(Purchaserequester, self).unlink()

    
        

    @api.depends('line_ids','line_ids.state')
    def _compute_state(self):
        for self in self:
            state = 'draft'
            states = set(self.line_ids.mapped('state'))
            if 'to_rectify' in states:
                state = 'to_rectify'                
            if 'rejected' in states and 'approve' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('rejected','approve')]
                if not r:
                    state = 'approve'
            if 'to_process' in states and 'approve' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('to_process','approve')]
                if not r:
                    state = 'to_process'            
            if 'approve' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('approve')]
                if not r:
                    state = 'approve'
            if 'rejected' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('rejected')]
                if not r:
                    state = 'rejected'
            if 'rejected' in states and 'to_process' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('to_process','rejected')]
                if not r:
                    state = 'to_process'
            if 'to_process' in states and 'to_rectify' not in states:                
                r = [x for x in states if x not in ('to_process')]
                if not r:
                    state = 'to_process'        
            self.state=state
        

    def draft_request_purchase(self):
        for line in self.line_ids:
            if line.state not in ('draft','to_process'):
                raise UserError('La solicitud de compra no se puede cancelar.')
            
        for line in self.purchase_order_id:
            if line.state != 'draft':
                raise UserError('La solicitud de compra no se puede cancelar.')
            if line.state == 'draft':
                line.sudo().button_cancel()
                line.sudo().unlink()            

        for line in self.line_ids:
            line.state = 'draft'


    def action_purchase(self):
        self.ensure_one()
        res_model_id = self.env['ir.model'].search(
            [('name', '=', self._description)]).id
        self.env['mail.activity'].create([{'activity_type_id': 4,
            'date_deadline': datetime.today(),
            'summary': "Solicitud de compra P001",
            'user_id': self.approver_id.id,
            'res_id': self.id,
            'res_model_id': res_model_id,
            'note': 'Solicitud de compra',
        }])
    
    def send_message(self):
        user_ids=[]
        user_ids.append(self.requested_by.partner_id.id)
        user_ids.append(self.approver_id.partner_id.id)
        mail_channel= self.env['mail.channel'].search([('active','=',True)])
        channel_id = False
        for line in mail_channel:
            if len(line.channel_member_ids) == 2:
                partner_ids = line.channel_member_ids.mapped('partner_id').ids
                if partner_ids == user_ids:
                    channel_id = line.id
                    break
        if channel_id == False:            
            new_channel = self.env['mail.channel'].create({
                'name': '%s, %s' % (self.requested_by.partner_id.name,self.approver_id.partner_id.name),
                'channel_type':'chat',
                'is_chat':True
             })            
            self.env['mail.channel.member'].create({
                'partner_id':self.approver_id.partner_id.id,
                'channel_id':new_channel.id
            })
            channel_id = new_channel.id
        mensage = """<div style="color:#5132b9; font-size:14px" ><br/>Apreciable <b>"%s"</b>, <b>"%s"</b> le acaba de enviar una <b>Solicitud de Compra</b>:<br/><br/>
                    ■ Documento de origen: <b>"%s"</b><br/></div>""" % (self.approver_id.name,self.requested_by.name,self.name)

        
        channel = self.env['mail.channel'].browse(channel_id)
        channel.sudo().message_post(body=mensage, author_id=self.env.user.partner_id.id)
        
    def make_purchase_quotation(self):
        self.send_message()
        for line in self.line_ids:
            line.apply_state_to_process()
        
    
    @api.depends('state')
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ['approve', 'to_process','rejected']:
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'purchase.requester') or '/'
        return super(Purchaserequester, self).create(vals)
    
