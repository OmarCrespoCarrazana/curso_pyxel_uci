# -*- coding: utf-8 -*-
{
    "name": "Nursery Requests",
    "summary": """ Childcare Management Nursery Request Module """,
    "description":
    """ 
    This module process all the requests made 
    by the nursery staff over Medical Supplies and Child Medication stock products
    """,
    "author": "LeudiX (Odoo Junior Developer)",
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
        "mail"],    # Messaging & Notifications for system users
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
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
