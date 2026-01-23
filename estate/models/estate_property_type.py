from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type model for the estate module."

    name = fields.Char(required=True)