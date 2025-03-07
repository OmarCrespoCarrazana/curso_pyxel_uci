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
        string="Requested by",
        related="request_id.nurse_id",
        store=True,
        readonly=True,
    )

    storekeeper_id = fields.Many2one(
        string=_("Processed by"),
        related="request_id.storekeeper_id",
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

    category_name = fields.Char(
        related="category_id.name",
        string=_("Category Name"),
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
        """Retrieve products from allowed categories, including subcategories
        with stock greater than zero."""
        allowed_categories = ["Nursing"]
        category_ids = (
            self.env["product.category"]
            .search([("complete_name", "ilike", allowed_categories[0])])
            .ids
        )
        # Create a domain to filter products by category and stock availability
        domain = [("categ_id", "in", category_ids), ("qty_available", ">", 0)]
        return domain

    @api.constrains("quantity")
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero"))

    @api.constrains("product_id", "request_id")
    def _check_duplicate_product(self):
        for line in self:
            # Search for other lines in the same request with the same product
            duplicate_lines = self.search(
                [
                    ("request_id", "=", line.request_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("id", "!=", line.id),  # Exclude the current line
                ]
            )
            if duplicate_lines:
                raise ValidationError(
                    f"The product {line.product_id.name} is already in the request. \n"
                    f"Please update the quantity instead of adding the same product again."
                )
