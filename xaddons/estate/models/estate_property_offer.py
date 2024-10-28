from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "房屋报价"

    price = fields.Float(string="报价金额")
    status = fields.Selection(
        [("draft", "草稿"), ("confirm", "已确认"), ("cancel", "已取消")],
        string="状态",
        default="draft",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="买家", required=True)
    property_id = fields.Many2one("estate.property", string="房源", required=True)

    validity = fields.Integer(string="有效天数", default=30)
    date_deadline = fields.Date(string="截止日期", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)


    def _inverse_date_deadline(self):
        self.validity = (self.date_deadline - self.create_date.date()).days