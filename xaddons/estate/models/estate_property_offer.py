from typing import Any
from odoo import models, fields, api, exceptions
from datetime import timedelta

from odoo.api import ValuesType


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
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)


    def _inverse_date_deadline(self):
        self.validity = (self.date_deadline - self.create_date.date()).days

    def do_accept(self):
        """
        接受报价
        """
        if self.status == "draft" and self.search_count(domain=[("status", "=", "confirm"), ("property_id", "=", self.property_id.id)]) == 0:
            self.status = "confirm"
            self.property_id.selling_price = self.price
            self.property_id.partner_id = self.partner_id
        else:
            raise exceptions.UserError("报价状态不正确，无法接受！")

    def do_cancel(self):
        """
        取消报价
        """
        if self.status == "draft":
            self.status = "cancel"
        else:
            raise exceptions.UserError("报价状态不正确，无法取消！")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            offers = self.search(domain=[("property_id", "=", vals["property_id"])])
            price = vals.get("price")
            if offers and price < max(offers.mapped("price")):
                raise exceptions.UserError("已有更低报价，请不要重复报价！")
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state=="available":
                property.state="received"
        return super().create(vals_list)