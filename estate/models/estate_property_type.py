from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type model for the estate module."

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name already exists!",
    )