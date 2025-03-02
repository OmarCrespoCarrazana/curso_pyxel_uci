
{
    'name': 'Employee',
    'version': '17.0.0.0.0',
    'summary': 'Employee management',
    'author': 'Pyxel SLR Odoo`s Trainees  Team',
    'category': 'Services',
    'depends': ['base', 'mail', 'hr', 'hr_contract'],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "reports/hr_contract_report.xml",
        "views/hr_contract_menu.xml",
        
        
    ],
    'installable': True,
    'application': True,
}
