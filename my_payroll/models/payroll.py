from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Payroll(models.Model):
    _name = 'my_payroll.payroll'
    _description = 'Nómina'

    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    base_salary = fields.Float(string='Salario Base', compute='_compute_base_salary', store=True)
    extra_salary = fields.Float(string='Pago por Horas Extras', compute='_compute_extra_salary', store=True)
    gross_salary = fields.Float(string='Salario Bruto', compute='_compute_gross_salary', store=True)
    deductions = fields.Float(string='Deducciones', help="Deducciones totales (impuestos, seguros, etc.)")
    bonuses = fields.Float(string='Bonificaciones', help="Bonificaciones totales (rendimiento, etc.)")
    net_salary = fields.Float(string='Salario Neto', compute='_compute_net_salary', store=True)
    payroll_date = fields.Date(string='Fecha de Nómina', default=fields.Date.today)


    @api.depends('employee_id')
    def _compute_base_salary(self):
        """Obtiene el salario base del contrato activo del empleado"""
        for record in self:
            contract = record.employee_id.contract_id
            record.base_salary = contract.wage if contract else 0.0

    @api.depends('employee_id', 'payroll_date')
    def _compute_extra_salary(self):
        """Calcula horas extras basado en asistencias y contrato"""
        for record in self:
            if not record.employee_id or not record.payroll_date:
                record.extra_salary = 0.0
                continue

            # Obtener contrato activo
            contract = record.employee_id.contract_id
            if not contract:
                record.extra_salary = 0.0
                continue

            # Definir rango de fechas del mes
            start_of_month = record.payroll_date.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            # Obtener asistencias del mes
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', start_of_month),
                ('check_out', '<=', end_of_month),
            ])

            extra_hours = attendances.overtime_hours
            record.extra_salary = extra_hours * 50

    def generate_monthly_payroll(self):
        today = fields.Date.today()

        if today.day != 1:
            return
        
        employees = self.env['hr.employee'].search([
            ('contract_id', '!=', False),
            ('contract_id.state', '=', 'open')
        ])

        for employee in employees:
            existing = self.search([
                ('employee_id', '=', employee.id),
                ('payroll_date', '=', today)
            ], limit=1)
            
            if not existing:
                self.create({
                    'employee_id': employee.id,
                    'payroll_date': today,
                })

    

    @api.depends('base_salary', 'extra_salary')
    def _compute_gross_salary(self):
        for record in self:
            record.gross_salary = record.base_salary + record.extra_salary

    @api.depends('gross_salary', 'deductions', 'bonuses')
    def _compute_net_salary(self):
        for record in self:
            record.net_salary = record.gross_salary - record.deductions + record.bonuses
