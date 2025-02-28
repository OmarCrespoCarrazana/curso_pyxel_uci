from odoo import models, fields

class ChildcareMedicalHistory(models.Model):
    _name = "childcare.medical.history"
    _description = "Historial Médico"

    child_id = fields.Many2one(
        "childcare.child", 
        "Niño", 
        required=True,
        ondelete="cascade"
    )
    allergies = fields.Text("Alergias")
    chronic_conditions = fields.Text("Condiciones Crónicas")
    emergency_contact_id = fields.Many2one("res.partner", "Contacto de Emergencia")
    vaccination_ids = fields.One2many(
        "childcare.vaccination", 
        "medical_history_id", 
        "Vacunas"
    )

class ChildcareVaccination(models.Model):
    _name = "childcare.vaccination"
    _description = "Registro de Vacunas"

    name = fields.Char("Vacuna", required=True)
    date = fields.Date("Fecha de Aplicación", required=True)
    medical_history_id = fields.Many2one(
        "childcare.medical.history", 
        "Historial", 
        ondelete="cascade"
    )