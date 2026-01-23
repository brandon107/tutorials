from odoo import fields, models
from dateutil.relativedelta import relativedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Property model for the estate module."

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('oreceived', 'Offer Received'), ('oaccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
        )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
        )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')]
        )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
        )
    seller_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self._uid
        )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
        )
    tag_ids=fields.Many2many(
        "estate.property.tag", string="Property Tag"
        )
    offer_ids=fields.One2many(
        "estate.property.offer", "partner_id", string="Property Offer"
    )

