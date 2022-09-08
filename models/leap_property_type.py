from odoo import models,fields,api

class PropertyType(models.Model):
    _name = "leap.property.type"
    _order = "name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('name_type_uniq', 'UNIQUE(name)', 'this name cant have two name ,this name exsist!')
    ]  
    property_ids = fields.One2many("leap.property","property_type_id")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many("leap.property.offer","property_type_id")
    offer_count= fields.Integer(compute="_compute_offer_count")
    


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self :
            record.offer_count = 0
            for offer in record.offer_ids :
                record.offer_count += 1
                
                    