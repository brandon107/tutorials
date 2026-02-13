from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type model for the estate module."
    _order = "sequence"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name already exists!",
    )

    sequence = fields.Integer('Sequence', default=1, help="Use this to help order property types.")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")