# -*- coding: utf-8 -*-
{
    "name": "Childcare Management",
    "summary": """ Childcare Management Module """,
    "description": """
    """,
    "author": "Pyxel SLR Odoo`s Trainees  Team",
    "website": "",
    "category": "Services",
    "version": "1.0",
    # any module necessary for this one to work correctly
    "depends": [
        "base",     # Core module (Users, Security, Models)
        "hr",       # Employees (Nurses & Storekeepers)
        "product",  # Product categories and minimal stock
        "purchase",  # Supply Procurement
        "stock",    # Inventory & Warehouse
        "mail"],    # Messaging & Notifications
    # always loaded
    "data": [
        "security/nursery_request_security.xml",  # Groups & Record Rules (MUST load before access rights)
        "security/ir.model.access.csv",  # Model Access Rights (Must load after groups are defined)
        "data/sequences.xml",
        "views/nursery_request_menu_views.xml",
        "views/nursery_request_views.xml",
        "views/actions.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
