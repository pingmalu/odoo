# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "estate",
    "version": "0.1",
    "category": "Sales/estate",
    "sequence": 15,
    "summary": "Track leads and close opportunities",
    "website": "https://malu.me",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users.xml",
        "views/estate_menus.xml",
    ],
    "depends": [
        "base",
    ],
}
