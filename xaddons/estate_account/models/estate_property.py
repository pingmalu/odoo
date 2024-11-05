from odoo import Command, models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def do_sold(self):
        """
        创建发票
        """
        print("do_sold")
        self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "name": "发票",
                "move_type": "out_invoice",
                "journal_id": 1,
                "date": fields.Date.today(),
                "line_ids": [
                    Command.create(
                        {
                            "name": "营业税",
                            "quantity": 1,
                            "price_unit": self.selling_price*0.05,
                        }
                    ),
                    Command.create(
                        {
                            "name": "手续费",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return super().do_sold()
