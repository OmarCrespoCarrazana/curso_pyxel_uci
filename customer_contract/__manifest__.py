
{
    'name': 'Customer Contract',
    'version': '17.0.0.0.0',
    'summary': 'Contract invoice managment',
    'author': 'Ing.José Ramón Fidalgo García, M.Sc.Yadira Ramírez Rodríguez',
    'category': 'Services',
    'depends': ['base', 'calendar', 'website', 'mail', 'account','payment', 'crm', 'childcare_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/cron_jobs.xml',
        'views/email_template.xml',
        'views/contract_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
} 

