from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag model for the estate module."

    name = fields.Char(required=True)