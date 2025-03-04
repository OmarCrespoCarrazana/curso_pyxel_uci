{
    'name': 'Nomina de la Guarderia',
    'version': '1.0',
    'summary': 'Manage payroll for daycare employees',
    'description': 'Module to manage payroll for employees in a daycare center.',
    'author': 'Yilber Serrano Figueredo',
    'category': 'Human Resources',
    'depends': ['hr'],
    "data": [
        "security/ir.model.access.csv",
        "reports/payroll_report.xml",
        "views/employee_views.xml",
        "views/payroll_views.xml",
        "views/payroll_report_views.xml",
        "data/payroll_data.xml",
        
    ],
    'installable': True,
    'application': True,
}