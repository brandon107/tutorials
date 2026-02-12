from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer model for the estate module."

    price = fields.Float()

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be positive!",
    )
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        "estate.property", string="Properties", required=True, ondelete="cascade"
    )

    validity = fields.Integer(string="Validity (days)", default=7)            
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'oaccepted':
                raise UserError("An offer has already been accepted for this property.")
            else:
                record.property_id.state = 'oaccepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
        return True
    
    def action_refuse(self):
        for record in self:
            if record.status == 'oaccepted':
                record.property_id.state = 'oreceived'
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
            record.status = 'refused'
        return True