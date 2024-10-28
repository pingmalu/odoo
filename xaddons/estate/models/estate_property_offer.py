from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "房屋报价"

    price = fields.Float(string="报价金额")
    status = fields.Selection([('draft', '草稿'), ('confirm', '已确认'), ('cancel', '已取消')], string="状态", default='draft', copy=False)
    partner_id = fields.Many2one('res.partner', string="买家", required=True)
    property_id = fields.Many2one('estate.property', string="房源", required=True)
