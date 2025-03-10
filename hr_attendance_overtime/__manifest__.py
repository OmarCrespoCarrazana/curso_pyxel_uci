# __manifest__.py
{
    'name': 'HR Attendance Overtime',
    'version': '1.0',
    'summary': 'Calculate overtime in attendance',
    'description': 'This module adds overtime calculation to the attendance module.',
    'author': 'Pyxel SLR Odoo`s Trainees  Team',
    'depends': ['hr_attendance'],
    'data': [
       "security/ir.model.access.csv",
    ],
    'installable': True,
    'application': True,
}