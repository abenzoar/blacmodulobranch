# -*- coding: utf-8 -*-
from odoo import api, fields, models, api, _

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

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_requester_id = fields.Many2one('purchase.requester', string='Solicitud de compra')
    requested_by = fields.Many2one('res.users', related='purchase_requester_id.requested_by', string='Solicitado por')
    pr_note = fields.Text(string="Nota de Solicitud de Compra")

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_requester_line_id = fields.Many2one('purchase.requester.line', string='Linea de solicitud de compra')
    state_pr = fields.Selection(string='Estado', selection=_STATES, related="purchase_requester_line_id.state" , readonly=True)
    payment_state = fields.Selection(string='Pago', selection=_PAYMENT, related="purchase_requester_line_id.payment_state" , readonly=True)
    

    def unlink(self):
        for self in self:
            if self.purchase_requester_line_id:
                self.purchase_requester_line_id.unlink()
        return super(PurchaseOrderLine, self).unlink()
    
    def apply_state_rejected(self):
        self.purchase_requester_line_id.state = 'rejected'
        self.send_message_msn('rejected')
    
    def apply_state_to_rectify(self):
        self.purchase_requester_line_id.state = 'to_rectify'
        self.send_message_msn('to_rectify')
        
    def apply_state_approve(self):
        self.purchase_requester_line_id.state = 'approve'
        self.send_message_msn('approve')
                
    
    def apply_state_to_process(self):
        self.purchase_requester_line_id.state = 'to_process'
        
    
    def send_message_msn(self,msn):
        user_ids=[]
        user_ids.append(self.purchase_requester_line_id.request_id.requested_by.partner_id.id)
        user_ids.append(self.purchase_requester_line_id.request_id.approver_id.partner_id.id)
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
                'name': '%s, %s' % (self.purchase_requester_line_id.request_id.requested_by.partner_id.name,self.purchase_requester_line_id.request_id.approver_id.partner_id.name),
                'channel_type':'chat',
                'is_chat':True
             })            
            self.env['mail.channel.member'].create({
                'partner_id':self.purchase_requester_line_id.request_id.approver_id.partner_id.id,
                'channel_id':new_channel.id
            })
            channel_id = new_channel.id
        
        mensage = ''
        if msn == 'to_rectify':
            mensage = '<div style="color:#cb9f00; font-size:14px" ><br/>El producto <b>"%s"</b> ha sido marcado a \
            rectificar, </b>documento de origen <b>"%s"</b><br/></div>' % (self.product_id.display_name,self.purchase_requester_line_id.request_id.name)
        if msn == 'approve':
            mensage = '<div style="color:#03ab00; font-size:14px" ><br/>El producto <b>"%s"</b> ha sido marcado a \
            aprobado, </b>documento de origen <b>"%s"</b><br/></div>' % (self.product_id.display_name,self.purchase_requester_line_id.request_id.name)
        if msn == 'rejected':
            mensage = '<div style="color:#bb0000; font-size:14px" ><br/>El producto <b>"%s"</b> ha sido marcado a \
            rechazado, </b>documento de origen <b>"%s"</b><br/></div>' % (self.product_id.display_name,self.purchase_requester_line_id.request_id.name)
        
        
        channel = self.env['mail.channel'].browse(channel_id)
        channel.sudo().message_post(body=mensage, author_id=self.env.user.partner_id.id)
    
