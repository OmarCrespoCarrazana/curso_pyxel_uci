# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NurseryRequestLine(models.Model):
    _name = "nursery.request.line"
    _description = "Nursery Request Line"
    _rec_name = "request_id"

    request_id = fields.Many2one(
        string=_("Nursery Request"),
        comodel_name="nursery.request",
        required=True,
        ondelete="cascade",
    )

    nurse_id = fields.Many2one(
        string="Nurse",
        related="request_id.nurse_id",
        store=True,
        readonly=True,
    )

    product_id = fields.Many2one(
        string=_("Product"),
        comodel_name="product.product",
        required=True,
        domain=lambda self: self._get_product_domain(),
    )

    category_id = fields.Many2one(
        string=_("Product Category"),
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
    )

    state = fields.Selection(
        related="request_id.state",
        string=_("Current State"),
        store=True,
        readonly=True,
    )

    quantity = fields.Float(string=_("Requested Quantity"), required=True)

    @api.model
    def _get_product_domain(self):
        """Retrieve products from allowed categories, including subcategories."""
        allowed_categories = ["Medical Supplies", "Child Medications"]
        category_ids = (
            self.env["product.category"]
            .search(
                [
                    "|",
                    ("complete_name", "ilike", allowed_categories[0]),
                    ("complete_name", "ilike", allowed_categories[1]),
                ]
            )
            .ids
        )

        return [("categ_id", "in", category_ids)]

    @api.constrains("quantity")
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero"))
