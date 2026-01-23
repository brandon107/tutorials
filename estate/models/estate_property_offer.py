from odoo import fields, models

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer model for the estate module."

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        "estate.property", string="Properties", required=True
    )
