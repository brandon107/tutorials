from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class Property(models.Model):
    _name = "estate.property"
    _description = "Property model for the estate module."

    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')]
    )
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('oreceived', 'Offer Received'), ('oaccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        readonly=True,
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
    facades = fields.Integer()
    garage = fields.Boolean()

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
        "estate.property.offer", "property_id", string="Property Offer"
    )

    best_price = fields.Integer(compute="_compute_best_price", string="Best Offer")
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = 'cancelled'
        return True

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive!",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive!",
    )

