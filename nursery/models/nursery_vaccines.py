from odoo import models, fields, api

class NurseryVaccines(models.Model):
    _name = 'nursery.vaccines'
    _description = 'vacunas aplicadas al niño'

    name = fields.Char(string="Nombre de la vacuna", required = True)