from odoo import models, fields, api, exceptions
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
        selection=[("available", "可售"), ("sold", "已售"), ("rented", "出租中"), ("cancel", "已取消")],
        default="available",
        copy=False,
        required=True,
        readonly=True
    )
    property_type_id = fields.Many2one(string="类型", comodel_name="estate.property.type")
    partner_id = fields.Many2one(string="买家", comodel_name="res.partner")
    sale_person_id = fields.Many2one(string="销售人员", comodel_name="res.users")
    tag_id = fields.Many2many(string="标签", comodel_name="estate.property.tag")
    offer_ids = fields.One2many(string="报价",inverse_name="property_id", comodel_name="estate.property.offer")

    total_area = fields.Float(compute="_compute_total_area", string="总面积")
    best_price = fields.Float(compute="_compute_best_price", string="最佳报价")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(offer.price for offer in record.offer_ids)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "south"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.onchange("bedrooms")
    def _onchange_bedrooms(self):
        if self.bedrooms > 5:
            warning = {
                'title': "警告",
                'message': "卧室数量异常"
            }
            return {'warning': warning}

    def do_sold(self):
        """
        将状态设置为已售
        """
        if self.state == "sold":
            raise exceptions.UserError("该物业已售出")
        else:
            self.state = "sold"


    def do_cancel(self):
        """
        将状态设置为已取消
        """
        if self.state == "cancel":
            raise exceptions.UserError("该物业已取消")
        else:
            self.state = "cancel"


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

    @api.constrains('expected_price','selling_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price * 0.9 > record.selling_price:
                raise exceptions.ValidationError("销售价格不能低于期望价格的90%")

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = ("%s (copy)") % (self.name)
        return super(self.__class__, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', '名称已存在'),
        ('expected_price', 'CHECK(expected_price>=0)', '期望价格必须大于等于0'),
        ('selling_price', 'CHECK(selling_price>=0)', '销售价格必须大于等于0'),
        ('living_area', 'CHECK(living_area>=0)', '使用面积必须大于等于0'),
        ('garden_area', 'CHECK(garden_area>=0)', '花园面积必须大于等于0'),
    ]
