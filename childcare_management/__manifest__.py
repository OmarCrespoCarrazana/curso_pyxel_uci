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
    "depends": ["base", "website", "hr", "product", "stock", "crm", "account", "mail", "portal"],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'templates/base_layout.xml',
        'templates/navbar.xml',
        'templates/footer.xml',
        'templates/breadcrumbs.xml',
        'templates/login_base.xml',
        'templates/login.xml',  # Asegúrate de que esté aquí y sin espacios
        'templates/dashboard.xml',
        'templates/children.xml',
        'templates/medical_records.xml',
        'templates/components/modal_base.xml',
        'templates/components/service_form.xml',
        'templates/services.xml',
        'templates/reusable_table.xml',
        'templates/invoices.xml',
    ],
    "assets": {
        "web.assets_backend": [
        ],
        "web.assets_frontend": [   
            ("include", "https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"),
            "/childcare_management/static/src/css/index.css",
        ],
        "web.assets_common": [
            ("include", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"),
        ]
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
