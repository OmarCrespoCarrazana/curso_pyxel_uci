{
    'name': 'Nomina de la Guarderia',
    'version': '1.0',
    'summary': 'Manage payroll for daycare employees',
    'description': 'Module to manage payroll for employees in a daycare center.',
    'author': 'Pyxel SLR Odoo`s Trainees  Team',
    'category': 'Human Resources',
    'depends': ['base', 'hr','hr_attendance'],
    "data": [
        "security/ir.model.access.csv",
        "views/employee_views.xml",
        "views/payroll_report.xml",
        "views/payroll_views.xml",
        "data/payroll_data.xml",
        
    ],
    'installable': True,
    'application': True,
}