from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "标签"

    name = fields.Char(string="标签", required=True)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = ("%s (copy)") % (self.name)
        return super(self.__class__, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', '名称已存在'),
    ]
