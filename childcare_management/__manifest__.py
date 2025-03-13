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
    "depends": ["base","child_base","nursery","web","mass_mailing", "website", "hr", "product", "stock", "crm", "account", "mail"],
    # always loaded
    "data": [
        'security/daycare_security.xml',
        'security/ir.model.access.csv',
        "views/child_views.xml",
        "views/classroom_views.xml",
        "views/child_attendance_views.xml",
        "views/employee_views.xml",
        "views/reports.xml",
        'templates/layouts/base_layout.xml',
        'templates/layouts/account_layout.xml',
        'templates/login/login_base.xml',
        'templates/components/modal_base.xml',
        'templates/components/navbar.xml',
        'templates/components/footer.xml',
        'templates/components/breadcrumbs.xml',
        'templates/login/login.xml',
        'templates/home.xml',
        'templates/dashboard/dashboard.xml',
        'templates/children/child_card.xml',
        'templates/children/child_detail.xml',
        'templates/children/children.xml',
        'templates//medical_records/medical_records.xml',
        'templates/components/reusable_table.xml',
        'templates/invoices/invoices.xml',
        'templates/account/portal_account.xml',
        'templates/account/account_security.xml',
        'templates/account/account_profile.xml',
      #  'data/cron_jobs.xml',
       
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
        ],
        "web.assets_frontend": [   
            'childcare_management/static/src/components/**/*.js',
            'childcare_management/static/src/components/**/*.xml',
            'childcare_management/static/src/components/geneic_table/**/*.js',
            'childcare_management/static/src/components/geneic_table/**/*.xml',    
        ],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
