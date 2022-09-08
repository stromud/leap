from odoo import models,fields


class PropertyTag(models.Model):
    _name = "leap.property.tag"
    _order = "name"


    name = fields.Char(required=True)
    color = fields.Integer()
    


    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'this name cant have two name ,this name exsist!')
    ]    
