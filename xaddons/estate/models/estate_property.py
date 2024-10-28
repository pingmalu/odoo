from odoo import models, fields
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(string="名称", required=True)
    street = fields.Char(string="小区")
    city = fields.Char(string="城市")
    description = fields.Text(string="描述")
    postcode = fields.Char(string="邮编")
    date_availability = fields.Date(
        string="可售日期",
        copy=False,
        default=lambda self: fields.Datetime.now() + timedelta(days=90),
    )
    expected_price = fields.Float(string="期望价格", required=True)
    selling_price = fields.Float(string="销售价格", readonly=True)
    bedrooms = fields.Integer(string="卧室数量", default=2)
    living_area = fields.Integer(string="使用面积")
    facades = fields.Integer(string="面")
    garage = fields.Boolean(string="是否有车库")
    garden = fields.Boolean(string="是否有花园")
    garden_area = fields.Integer(string="花园面积")
    garden_orientation = fields.Selection(
        string="花园方向",
        selection=[("north", "北"), ("south", "南"), ("east", "东"), ("west", "西")],
    )
    active = fields.Boolean(string="有效", default=True)
    state = fields.Selection(
        string="状态",
        selection=[("available", "可售"), ("sold", "已售"), ("rented", "出租中")],
        default="available",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(string="类型", comodel_name="estate.property.type")
    owner_id = fields.Many2one(string="业主", comodel_name="res.partner")
    sale_person_id = fields.Many2one(string="销售人员", comodel_name="res.users")
    tag_id = fields.Many2many(string="标签", comodel_name="estate.property.tag")
    offer_ids = fields.One2many(string="报价",inverse_name="property_id", comodel_name="estate.property.offer")
    # property_type = fields.Selection(
    #     string="类型",
    #     selection=[
    #         ("house", "房屋"),
    #         ("apartment", "公寓"),
    #         ("office", "办公室"),
    #         ("store", "商铺"),
    #         ("condo", "别墅"),
    #         ("villa", "别墅"),
    #         ("land", "土地"),
    #     ],
    # )
    # owner_id = fields.Many2one(
    #     "res.partner", string="业主", required=True, ondelete="restrict"
    # )
    # agent_id = fields.Many2one(
    # )
    # images = fields.Binary(string="图片")
    # video = fields.Binary(string="视频")
    # location_id = fields.Many2one(
    #     "res.partner", string="位置", required=True, ondelete="restrict"
    # )
    # property_id = fields.Many2one(
    #     "estate.property", string="物业", required=True, ondelete="restrict"
    # )
    # property_ids = fields.Many2many(
    #     "estate.property", string="物业", required=True, ondelete="restrict"
    # )
    # rent_ids = fields.One2many(
    #     "estate.rent", "property_id", string="出租信息"
    # )
    # sale_ids = fields.One2many(
    #     "estate.sale", "property_id", string="售卖信息"
    # )

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = ("%s (copy)") % (self.name)
        return super(self.__class__, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', '名称已存在'),
    ]
