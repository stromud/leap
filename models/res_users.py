from odoo import fields,models 


class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('leap.property','user_id')


