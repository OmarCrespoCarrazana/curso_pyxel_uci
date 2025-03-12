from odoo import models, fields

class OphthalmologyExam(models.Model):
    _name = "ophthalmology.exam"
    _description = "Examen de Oftalmología"

    clinical_history_id = fields.Many2one("nursery.clinical.history", string="Historia Clínica")
    date = fields.Date(string="Fecha", required=True)
    vision_test = fields.Char(string="Prueba de Visión")
    eye_pressure = fields.Float(string="Presión Ocular")
    notes = fields.Text(string="Observaciones")

class StomatologyExam(models.Model):
    _name = "stomatology.exam"
    _description = "Examen de Estomatología"

    clinical_history_id = fields.Many2one("nursery.clinical.history", string="Historia Clínica")
    date = fields.Date(string="Fecha", required=True)
    dental_health = fields.Text(string="Salud Dental")
    gum_health = fields.Text(string="Salud de las Encías")
    notes = fields.Text(string="Observaciones")

class HemogramExam(models.Model):
    _name = "hemogram.exam"
    _description = "Examen de Hemograma"

    clinical_history_id = fields.Many2one("nursery.clinical.history", string="Historia Clínica")
    date = fields.Date(string="Fecha", required=True)
    red_blood_cells = fields.Float(string="Glóbulos Rojos")
    white_blood_cells = fields.Float(string="Glóbulos Blancos")
    platelets = fields.Float(string="Plaquetas")
    hemoglobin = fields.Float(string="Hemoglobina")
    notes = fields.Text(string="Observaciones")

class FecesExam(models.Model):
    _name = "feces.exam"
    _description = "Examen de Heces Fecales"

    clinical_history_id = fields.Many2one("nursery.clinical.history", string="Historia Clínica")
    date = fields.Date(string="Fecha", required=True)
    parasites = fields.Char(string="Presencia de Parásitos")
    consistency = fields.Char(string="Consistencia")
    color = fields.Char(string="Color")
    notes = fields.Text(string="Observaciones")

class UrineExam(models.Model):
    _name = "urine.exam"
    _description = "Examen de Orina"

    clinical_history_id = fields.Many2one("nursery.clinical.history", string="Historia Clínica")
    date = fields.Date(string="Fecha", required=True)
    ph = fields.Float(string="pH")
    proteins = fields.Char(string="Proteínas")
    glucose = fields.Char(string="Glucosa")
    notes = fields.Text(string="Observaciones")
