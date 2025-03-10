# -*- coding: utf-8 -*-
{
    "name": "Childcare Base",
    "summary": """ Childcare Base Module """,
    "description": """
    """,
    "author": "Pyxel SLR Odoo`s Trainees  Team",
    "website": "",
    "category": "Services",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base","web","mass_mailing", "website", "hr", "product", "stock", "crm", "account", "mail"],
    # always loaded
    "data": [
     #   'security/ir.model.access.csv',
        "views/partner_views.xml",
        'data/cron_jobs.xml',
       
    ],
    # only loaded in demonstration mode
    "demo": [
    #    "demo/demo.xml",
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
