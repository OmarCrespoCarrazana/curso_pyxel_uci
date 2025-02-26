# -*- coding: utf-8 -*-
{
    "name": "Childcare Management",
    "summary": """ Childcare Management Module """,
    "description": """
    """,
    "author": "Pyxel SLR Odoo`s Trainees  Team",
    "website": "",
    "category": "Services",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "website", "hr", "product", "stock", "crm", "account", "mail"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_frontend": [],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
