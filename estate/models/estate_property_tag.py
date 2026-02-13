from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag model for the estate module."
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Tag name already exists!",
    )