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
