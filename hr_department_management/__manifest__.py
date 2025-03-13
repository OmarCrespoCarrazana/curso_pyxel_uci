{
    'name': 'Gestión de Departamentos (Extensión)',
    'version': '1.0',
    'summary': 'Extensión del módulo de Departamentos',
    'description': 'Nuevas funcionalidades para los departamentos de la guarderia',
    'author': 'Yilber Serrano Figueredo',
    'category': 'Human Resources',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/hr_department_wizard_views.xml',
        'reports/hr_department_report.xml',
        'views/hr_department_report_views.xml',
    ],
    'installable': True,
    'application': True,
}