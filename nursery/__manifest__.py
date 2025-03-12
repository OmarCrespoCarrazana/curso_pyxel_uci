# -*- coding: utf-8 -*-
{
    'name': "nursery",

    'summary': "nursery mngmt module",

    'description': """Long description of module's purpose""",

    'author': "Pyxel SLR Odoo`s Trainees  Team",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Services",
    'version': '0.1',

    # any module necessary for this one to work correctly
    "depends": ["base", "website", "hr", "product", "stock", "crm", "account", "mail", "child_base"],

    # always loaded
    'data': [        
        'security/nursery_security.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'data/sequences.xml',
        'data/vaccines.xml',
        'views/nursery_clinical_history_views.xml',
        'views/nursery_medical_event_views.xml',
        'views/nursery_medical_supply_views.xml',
        'views/nursery_vaccines_views.xml',
        'views/nursery_menu_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
