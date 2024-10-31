from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "房屋类型"
    _order = "sequence"

    name = fields.Char(string="房屋类型", required=True)
    sequence = fields.Integer(string="排序",help="用于显示房屋类型时的顺序")

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = ("%s (copy)") % (self.name)
        return super(self.__class__, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', '名称已存在'),
    ]
