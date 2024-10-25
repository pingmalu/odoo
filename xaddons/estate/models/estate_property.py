from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="描述")
    postcode = fields.Char(string="邮编")
    date_availability = fields.Date(string="可售日期")
    expected_price = fields.Float(string="期望价格", required=True)
    selling_price = fields.Float(string="销售价格")
    bedrooms = fields.Integer(string="卧室数量")
    living_area = fields.Integer(string="使用面积")
    facades = fields.Integer(string="面")
    garage = fields.Boolean(string="是否有车库")
    garden = fields.Boolean(string="是否有花园")
    garden_area = fields.Integer(string="花园面积")
    garden_orientation = fields.Selection(
        string="花园方向",
        selection=[("north", "北"), ("south", "南"), ("east", "东"), ("west", "西")],
    )
