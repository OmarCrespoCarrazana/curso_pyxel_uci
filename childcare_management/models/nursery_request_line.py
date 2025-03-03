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
        domain=lambda self: [("categ_id", "in", self._get_nursery_category_ids())],
    )
    quantity = fields.Float(string=_("Requested Quantity"), required=True)

    @api.constrains("quantity")
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero"))

    @api.model
    def _get_nursery_category_ids(self):
        """Retrieve nursery related category IDs dynamically instead of hardcoding names"""
        categories = self.env["product.category"].search(
            [
                "|",
                ("complete_name", "ilike", "Medical Supplies"),
                ("complete_name", "ilike", "Child Medications"),
            ]
        )
        return categories.ids

    @api.model
    def default_get(self, fields_list):
        """Ensure request_id is auto-filled when adding a new request line."""
        defaults = super().default_get(fields_list)
        if self.env.context.get("default_request_id"):
            defaults["request_id"] = self.env.context["default_request_id"]
        return defaults
