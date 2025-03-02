# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date

_logger = logging.getLogger(__name__)


class NurseryRequest(models.Model):
    _name = "nursery.request"
    _description = "Nursery Medical Supply Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # Enable notifications
    _rec_name = "name"

    # Ensures unique reference per request
    name = fields.Char(
        string="Request Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    nurse_id = fields.Many2one(
        string=_("Requested by"),
        comodel_name="hr.employee",
        required=True,
        default=lambda self: self.env.user.employee_id.id,
    )
    doctor_id = fields.Many2one(
        "hr.employee",
        string="Doctor Approval",
        required=True,
    )
    date_requested = fields.Datetime(string="Request Date", default=fields.Datetime.now)
    date_processed = fields.Datetime(string="Process Date")
    state = fields.Selection(
        [("draft", "Draft"), ("denied", "Denied"), ("approved", "Approved")],
        string="Status",
        default="draft",
        tracking=True,
    )
    request_line_ids = fields.One2many(
        string=_("Requested Items"),
        comodel_name="nursery.request.line",
        inverse_name="request_id",
    )

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("nursery.request") or _(
                "New"  # Generating sequence when saving a Nursery request
            )
        return super(NurseryRequest, self).create(vals)

    def action_approve(self):
        for request in self:
            for line in request.request_line_ids:
                if line.product_id.categ_id.name not in [
                    "Medical Supplies",
                    "Child Medications",
                ]:
                    raise UserError(
                        _(
                            "Only medical supplies and child medications can be requested."
                        )
                    )
                if line.product_id.qty_available < line.quantity:
                    raise UserError(
                        _(
                            "Requested quantity for %s exceeds stock."
                            % line.product_id.name
                        )
                    )
                # Deduct from stock
                line.product_id.sudo().write(
                    {"qty_available": line.product_id.qty_available - line.quantity}
                )
                request.write({"state": "approved"})
                request.write({"date_processed": "%s" % date.today().strftime('%Y-%m-%d')})
                # Notifying both nurse and doctor
                request.message_post(
                    body=_("Your request for product: %s has been approved." % line.product_id.name),
                    partner_ids=[request.nurse_id.partner_id.id],
                )
                request.message_post(
                    body=_("A request you approved for product: %s has been processed." % line.product_id.name),
                    partner_ids=[request.doctor_id.partner_id.id],
                )

    def action_deny(self):
        for request in self:
            request.write({"state": "denied"})
            # Notifying both nurse and doctor
            request.message_post(
                body=_("Your request has been denied."),
                partner_ids=[request.nurse_id.partner_id.id],
            )
            request.message_post(
                body=_("A request you approved has been denied."),
                partner_ids=[request.doctor_id.partner_id.id],
            )


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
        domain=[("categ_id.name"), "in", ["Medical Supplies", "Child Medications"]],
    )
    quantity = fields.Float(string=_("Requested Quantity"), required=True, default=1)

    @api.constrains("quantity")
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero"))
