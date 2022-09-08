from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name ="leap.property.offer"
    _order ="price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted','Accepted'),
            ('refused','Refused'),
            ('received','Received')
        ],
        default='received'
    )
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('leap.property',required=True)
    validity= fields.Integer(default=7)
    date_deadline= fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    create_date = fields.Date(default = lambda self: fields.Date.today())
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)


    def _inverse_date_deadline(self):
        for record in self :
            record.validity = (record.date_deadline - record.create_date).days
            
    def accepted_action(self):
        
        for record in self :
            if record.status != 'refused' and record.property_id.state in ['new','received'] :
                record.status = 'accepted'
                record.property_id.state = "accepted"
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price




    def refused_action(self):
        for record in self:
            if record.status != 'accepted' :
                record.status = 'refused'

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'price must to be positive.')
    ]
    
    @api.model
    def create(self,vals):
        appog = self.env['leap.property'].browse(vals['property_id'])
        for record in appog:
            for recordoffer in record.offer_ids:
                if recordoffer.price > vals['price']:
                    raise UserError("you cant create offer with this price")
            if appog.state == 'new':
                appog.state = 'received' 
        return super(PropertyOffer,self).create(vals)  

            





