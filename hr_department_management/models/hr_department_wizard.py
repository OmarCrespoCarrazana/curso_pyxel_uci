from odoo import models, fields, api

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