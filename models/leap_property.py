from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,exceptions
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError





class Property(models.Model):
    _name ="leap.property"
    _description = "Agenzia immobiliare"
    _order ="id desc"


    name = fields.Char(required=True,)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default = lambda self: fields.Date.today() + relativedelta(months = 3))
    expected_price = fields.Float(required=True,)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facedes = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area =fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection = [
            ('n','Nord'),
            ('s','South'),
            ('e','East'),
            ('w','West'),
            
        ]
    )
    state = fields.Selection(
        selection = [
            ('new','New'),
            ('received','Offer Received'),
            ('accepted','Offer Accepted'),
            ('sold','Sold'),
            ('canceled','Canceled'),

        ],
        default='new',
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one("leap.property.type")
    partner_id = fields.Many2one('res.partner',string="buyer",copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson',default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('leap.property.tag')
    offer_ids = fields.One2many('leap.property.offer','property_id')
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    statusbar = fields.Char(compute="_compute_statusbar")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
        

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0.0
            for offer in record.offer_ids :
                if offer.price > record.best_price :
                    record.best_price = offer.price

    @api.onchange("garden")
    def _onchenge_garden_area(self):
        if self.garden == True :
            self.garden_area = 10
            self.garden_orientation = 'n'
        else :
            self.garden_area = 0
            self.garden_orientation = 0

    def sold_action(self):
        for record in self :
            if record.state == 'accepted':
                record.state = 'sold'


    def cancel_action(self):
        for record in self :
            if record.state != 'sold':
                record.state = 'canceled'
            else :
                raise exceptions.UserError("this property can't be canceled")

                
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'expected price must to be positive.'),
         ('check_selling_price', 'CHECK(selling_price > 0)',
         'selling price must to be positive.')
    ]

    @api.constrains('selling_price')
    def percenter_price(self):
        for percent in self:
            if percent.selling_price < (percent.expected_price * 90)/100:
                raise ValidationError("selling price cannot be lower than 90% of the expected price.")


    @api.onchange("offer_ids")
    def onchange_offer_received(self):
        for record in self:
            if len(record.offer_ids) > 0 and record.state == 'new':
                record.state = 'received'



    def unlink(self):
        for record in self:
            if record.state not in ('new','canceled'):
                raise exceptions.UserError("this property can't be delet")
        return super(Property,self).unlink()

        #voglio vedere se funziona


     