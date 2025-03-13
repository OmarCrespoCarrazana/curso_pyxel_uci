from odoo import models, fields, api
from odoo.exceptions import UserError

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    codigo = fields.Char(string='Código del Departamento',required=True,copy=False,unique=True,readonly=True,default=lambda self: self._generate_codigo(),)
    centro_costo = fields.Char(string='Centro de Costo', required=True)
    area_nomina = fields.Char(string='Área de Nómina', required=True)
    state = fields.Selection([('active', 'Activo'), ('inactive', 'Inactivo')], string='Estado', default='active', readonly= True)
    deactivation_date = fields.Date(string='Fecha de Desactivación', readonly=True)

    @api.model
    def _generate_codigo(self):
        """
        Genera un código único en formato AÑO/MES/SECUENCIAL (por ejemplo, 231001).
        """
        today = fields.Date.today()
        year = str(today.year)[-2:] 
        month = f"{today.month:02d}"  

        last_code = self.search(
            [('codigo', 'like', f"{year}{month}")],
            order='codigo DESC',
            limit=1,
        ).codigo

        if last_code:
            sequential = int(last_code[-3:]) + 1
        else:
            sequential = 1 

        codigo = f"{year}{month}{sequential:03d}"
        return codigo

    @api.model
    def create(self, vals):
        """
        Sobrescribe el método create para asegurar que el código se genere automáticamente.
        """
        if 'codigo' not in vals or not vals['codigo']:
            vals['codigo'] = self._generate_codigo()
        return super(HrDepartment, self).create(vals)


    def action_change_state(self):
        """Método para abrir la ventana emergente de confirmación."""
        self.ensure_one()
        if self.state == 'active':
            message = "¿Está seguro de desactivar este departamento?"
            new_state = 'inactive'
        else:
            message = "¿Está seguro de reactivar este departamento?"
            new_state = 'active'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirmar Cambio de Estado',
            'res_model': 'hr.department.confirm.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_department_id': self.id,
                'default_message': message,
                'default_new_state': new_state,
            },
        }
    def action_open_report_wizard(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generar Informe de Plantilla',
            'res_model': 'hr.department.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_department_id': self.id,
            },
        }

class HrDepartmentConfirmWizard(models.TransientModel):
    _name = 'hr.department.confirm.wizard'
    _description = 'Confirmación de Cambio de Estado'

    department_id = fields.Many2one('hr.department', string='Departamento', required=True)
    message = fields.Text(string='Mensaje', readonly=True)
    new_state = fields.Selection(
        [('active', 'Activo'), ('inactive', 'Inactivo')],
        string='Nuevo Estado',
        readonly=True
    )

    def action_confirm(self):
        """Confirma el cambio de estado."""
        self.ensure_one()
        department = self.department_id
        if self.new_state == 'inactive':
            department.write({
                'state': 'inactive',
                'deactivation_date': fields.Date.today(),
            })
        elif self.new_state == 'active':
            department.write({
                'state': 'active',
                'deactivation_date': False,
            })
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """Cancela la operación."""
        return {'type': 'ir.actions.act_window_close'}

class HrDepartmentReportWizard(models.TransientModel):
    _name = 'hr.department.report.wizard'
    _description = 'Wizard de Generación de Informe de Plantilla'

    department_id = fields.Many2one(
        'hr.department',
        string='Departamento',
        required=True,
        domain="[('state', '=', 'active')]"
    )

    def action_generate_report(self):
        # Obtener los datos del departamento y sus empleados
        department = self.department_id
        employees = self.env['hr.employee'].search([('department_id', '=', department.id)])

        # Preparar los datos para el informe
        report_data = {
            'department_name': department.name or 'Sin nombre',
            'centro_costo': department.centro_costo or 'No especificado',
            'area_nomina': department.area_nomina or 'No especificado',
            'employees': [{
                'id_empleado': employee.id_empleado or 'N/A',
                'name': employee.name or 'N/A',
                'surnames': employee.surnames or 'N/A',
                'job_title': employee.job_title or 'N/A',
            } for employee in employees],
        }

        # Generar el informe en PDF
        return self.env.ref('hr_department_management.action_hr_department_report').report_action(self, data=report_data)