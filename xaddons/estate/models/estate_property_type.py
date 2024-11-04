from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "房屋类型"
    _order = "sequence"

    name = fields.Char(string="房屋类型", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="房屋列表")
    sequence = fields.Integer(string="排序",help="用于显示房屋类型时的顺序")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="房屋报价列表")
    offer_count = fields.Integer(compute="_compute_offer_count", string="报价数量")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = ("%s (copy)") % (self.name)
        return super(self.__class__, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', '名称已存在'),
    ]
