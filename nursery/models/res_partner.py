import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    is_doctor = fields.Boolean(string='Es doctor')