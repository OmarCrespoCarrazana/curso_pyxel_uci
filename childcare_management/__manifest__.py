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
    "depends": ["base","mass_mailing", "website", "hr", "product", "stock", "crm", "account", "mail"],
    # always loaded
    "data": [
        'security/daycare_security.xml',
        'security/ir.model.access.csv',
        "views/child_views.xml",
        "views/classroom_views.xml",
        "views/child_attendance_views.xml",
       
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
