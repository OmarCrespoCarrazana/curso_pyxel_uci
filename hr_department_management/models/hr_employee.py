from odoo import models, fields, api
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    centro_costo = fields.Char(string='Centro de Costo', compute="_compute_centro_costo_area_nomina", store=True)
    area_nomina = fields.Char(string='Área de Nómina', compute="_compute_centro_costo_area_nomina", store=True)

    @api.depends('department_id.centro_costo', 'department_id.area_nomina')
    def _compute_centro_costo_area_nomina(self):
        """
        Calcula y guarda el centro de costo y el área de nómina basados en el departamento asignado.
        """
        for employee in self:
            if employee.department_id:
                employee.centro_costo = employee.department_id.centro_costo
                employee.area_nomina = employee.department_id.area_nomina
            else:
                employee.centro_costo = False
                employee.area_nomina = False
                
    @api.model
    def create(self, vals):
        """Validar que el departamento esté activo al crear un empleado."""
        if 'department_id' in vals:
            department = self.env['hr.department'].browse(vals['department_id'])
            if department.state == 'inactive':
                raise UserError("No se puede asignar un empleado a un departamento inactivo.")
        return super(HrEmployee, self).create(vals)

    def write(self, vals):
        """Validar que el departamento esté activo al actualizar un empleado."""
        if 'department_id' in vals:
            department = self.env['hr.department'].browse(vals['department_id'])
            if department.state == 'inactive':
                raise UserError("No se puede asignar un empleado a un departamento inactivo.")
        return super(HrEmployee, self).write(vals)