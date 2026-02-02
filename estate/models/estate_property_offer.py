from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

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

    validity = fields.Integer(string="Validity (days)", default=7, copy=False, required=True)            
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