from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Payroll(models.Model):
    _name = 'my_payroll.payroll'
    _description = 'Nómina'

    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    base_salary = fields.Float(string='Salario Base', default=500.0, readonly=True)
    extra_salary = fields.Float(string='Pago por Horas Extras', compute='_compute_extra_salary', store=True)
    gross_salary = fields.Float(string='Salario Bruto', compute='_compute_gross_salary', store=True)
    deductions = fields.Float(string='Deducciones', help="Deducciones totales (impuestos, seguros, etc.)")
    bonuses = fields.Float(string='Bonificaciones', help="Bonificaciones totales (rendimiento, etc.)")
    net_salary = fields.Float(string='Salario Neto', compute='_compute_net_salary', store=True)
    payroll_date = fields.Date(string='Fecha de Nómina', default=fields.Date.today)

   
    @api.depends('employee_id')
    def _compute_extra_salary(self):
        """
        Metodo de prueba para el calculo de salario manual
        """
        for record in self:
            # Obtener las asistencias del empleado en el mes actual
            start_of_month = record.payroll_date.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', start_of_month),
                ('check_out', '<=', end_of_month),
            ])

            # Calcular horas trabajadas y horas extras
            total_hours = sum(attendance.worked_hours for attendance in attendances)
            regular_hours = 280  # Horas al mes (supuesto)
            extra_hours = max(total_hours - regular_hours, 0)

            record.extra_salary = extra_hours * 50.0

    @api.model
    def generate_monthly_payroll(self):
        """
        Método para generar la nómina de manera automática el primer día de cada mes.
        """
        # Obtener la fecha actual
        today = datetime.today()
        first_day_of_month = today.replace(day=1)

        employees = self.env['hr.employee'].search([])

        # Recorrer cada empleado y generar su nómina
        for employee in employees:

            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', first_day_of_month),
                ('check_out', '<', first_day_of_month + timedelta(days=32)),
            ])
            total_hours = sum(attendance.worked_hours for attendance in attendances) if attendances else 0
            regular_hours = 280
            extra_hours = max(total_hours - regular_hours, 0)

            # Crear la nómina para el empleado
            self.create({
                'employee_id': employee.id,
                'extra_hours': extra_hours,
                'deductions': 0,  
                'bonuses': 0,      
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



class ReportWizard(models.TransientModel):
    _name = 'my_payroll.report.wizard'
    _description = 'Wizard de Generación de Informe de Nómina'

    month = fields.Selection(
        selection=[
            ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), 
            ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
            ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'),
            ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ],
        string='Mes',
        required=True
    )
    
    year = fields.Integer(
        string='Año',
        default=lambda self: int(datetime.now().year),
        required=True
    )

    @api.model
    def _get_payroll_data(self):
        print("=== INICIANDO BUSQUEDA DE DATOS ===")
        print("Datos del wizard:", self.read())
        print("Período seleccionado:", self.year, self.month)

        domain = [
            ('payroll_date', '>=', f"{self.year}-{self.month}-01"),
            ('payroll_date', '<=', 
                (datetime.strptime(
                    f"{self.year}-{self.month}-01", '%Y-%m-%d'
                ) + relativedelta(months=1) - timedelta(days=1)).strftime('%Y-%m-%d')
            )
        ]
        print("Dominio de búsqueda:", domain)
        # Verificar si hay registros
        payrolls = self.env['my_payroll.payroll'].search_read(domain)
        print("Cantidad de registros encontrados:", len(payrolls))
        print("Primer registro encontrado:", payrolls[0] if payrolls else "No hay registros")
        
        return payrolls

    def _prepare_report_data(self, payrolls):

        print("=== PREPARANDO DATOS PARA EL REPORTE ===")
        print("Registros encontrados:", len(payrolls))
        
        if not payrolls:
            print("No hay registros para el período seleccionado")
            raise ValidationError("No hay registros para el período seleccionado")
        
        report_data = {
            'docs': [{
                'id_empleado': payroll['employee_id'][0],
                'name': payroll['employee_id'][1],
                'gross_salary': payroll['gross_salary'],
                'deductions': payroll['deductions'],
                'bonuses': payroll['bonuses'],
                'net_salary': payroll['net_salary'],
                'payroll_date': payroll['payroll_date']
            } for payroll in payrolls]
        }
        print("Datos para el reporte:", report_data)
        return report_data


    def action_generate_report(self):
        print("=== INICIANDO GENERACIÓN DEL REPORTE ===")
        try:
            # Obtener los datos de nómina
            payrolls = self._get_payroll_data()
            
            # Validar si hay registros
            if not payrolls:
                raise ValidationError(
                    f"No hay registros de nómina para el mes {self.month}/{self.year}"
                )
                
            # Preparar los datos para el reporte
            report_data = self._prepare_report_data(payrolls)
            
            # Generar el reporte PDF
            return self.env.ref('my_payroll.action_report_payroll').report_action(
                self,
                data=report_data
            )
            
        except Exception as e:
            raise ValidationError(f"Error al generar el reporte: {str(e)}")