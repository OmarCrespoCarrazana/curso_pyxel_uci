# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class NurseryRequest(models.Model):
    _name = "nursery.request"
    _description = "Nursery Medical Supply Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # Enable notifications
    _rec_name = "name"

    # Ensures unique reference per request
    name = fields.Char(
        string="Request Code",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("nursery.request"),
    )
    nurse_id = fields.Many2one(
        string=_("Requested by"),
        comodel_name="hr.employee",
        required=True,
        default=lambda self: self.env.user.employee_id.id,
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
        return super(NurseryRequest, self).create(vals)

    def action_approve(self):
        for request in self:
            for line in request.request_line_ids:
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
                request.write({"date_processed": "%s" % fields.Datetime.now()})
                # Notifying the nurse
                if (
                    request.nurse_id
                    and request.nurse_id.user_id
                    and request.nurse_id.user_id.partner_id
                ):
                    request.message_post(
                        body=_(
                            "Your request for product: %s has been approved."
                            % line.product_id.name
                        ),
                        partner_ids=[request.nurse_id.user_id.partner_id.id],
                    )
                else:
                    _logger.warning(
                        "No valid partner found for the nurse on request %s",
                        request.id,
                    )

    def action_deny(self):
        for request in self:
            request.write({"state": "denied"})
            request.write({"date_processed": "%s" % fields.Datetime.now()})
            # Notifying the nurse
            if (
                request.nurse_id
                and request.nurse_id.user_id
                and request.nurse_id.user_id.partner_id
            ):
                request.message_post(
                    body=_("Your request has been denied."),
                    partner_ids=[request.nurse_id.user_id.partner_id.id],
                )
            else:
                _logger.warning(
                    "No valid partner found for the nurse on request %s",
                    request.id,
                )
