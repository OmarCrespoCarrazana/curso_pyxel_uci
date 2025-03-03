# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NurseryRequestLine(models.Model):
    _name = "nursery.request.line"
    _description = "Nursery Request Line"

    request_id = fields.Many2one(
        string=_("Request reference"),
        comodel_name="nursery.request",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string=_("Product"),
        comodel_name="product.product",
        required=True,
        # Retrieve only products from this categories
        # domain=[("categ_id.complete_name"), "in", ["Medical Supplies", "Child Medications"]],
    )
    quantity = fields.Float(string=_("Requested Quantity"), required=True)

    @api.constrains("quantity")
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero"))
