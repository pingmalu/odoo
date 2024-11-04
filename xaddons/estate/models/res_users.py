from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit ='res.users'

    property_ids = fields.One2many('estate.property', 'sale_person_id')