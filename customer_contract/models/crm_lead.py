from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    child_id = fields.Many2one("childcare.child", string="Niño")

    
    def _create_contract(self,lead):
        contract_model = self.env['customer.contract']
        for lead in self:
            if lead.stage_id.is_won and not contract_model.search([('lead_id','=', lead.id)]):
                lead.child_id.action_assign_best_classroom()
                contract_model.create({
                    'partner_id': lead.partner_id.id,
                    'lead_id': lead.id,
                })
    
    
    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals:
            for lead in self:
                if lead.stage_id.is_won:
                    lead._create_contract(lead)
        return res