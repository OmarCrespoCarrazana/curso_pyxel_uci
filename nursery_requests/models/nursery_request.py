# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        string=("Requested by"),
        comodel_name="hr.employee",
        required=True,
        default=lambda self: self.env.user.employee_id,
    )
    storekeeper_id = fields.Many2one(
        string=("Processed by"),
        comodel_name="hr.employee",
        required=False,
    )

    date_requested = fields.Datetime(string="Request Date", default=fields.Datetime.now)
    date_processed = fields.Datetime(string="Process Date")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("canceled", "Canceled"),
            ("pending", "Pending"),
            ("approved", "Approved"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    request_line_ids = fields.One2many(
        string=("Requested Items"),
        comodel_name="nursery.request.line",
        inverse_name="request_id",
    )

    def _get_notification_recipients(self):  # Helper Method
        """Returns the users in Admin and Storekeeper groups."""
        admin_group = self.env.ref("base.group_system", raise_if_not_found=False)
        storekeeper_group = self.env.ref(
            "nursery_requests.group_storekeeper", raise_if_not_found=False
        )
        return (
            (admin_group.users | storekeeper_group.users)
            if admin_group and storekeeper_group
            else self.env["res.users"]
        )

    @api.model
    def create(self, vals):
        """Ensures at least one product is added before creating a request and notifies storekeepers and admins."""
        if "request_line_ids" not in vals or not vals["request_line_ids"]:
            raise ValidationError(
                "You must add at least one product to create a nursing request."
            )
        # Ensure each line has a product
        for line in vals["request_line_ids"]:
            if not line[2].get("product_id"):
                raise ValidationError("All request lines must have a selected product.")

        # Create the request first
        request = super(NurseryRequest, self).create(vals)
        recipients = self._get_notification_recipients()
        message_body = ("A new nursing request %s has been created by %s.") % (
            request.name,
            request.nurse_id.name,
        )
        request.message_post(
            body=message_body,
            subtype_xmlid="mail.mt_comment",
            partner_ids=recipients.mapped("partner_id").ids,  # Send notifications
        )
        return request  # Return the created request

    @api.model
    def write(self, vals):
        """Process products updates on nursery requests when editing & notifies Admins & Storekeepers."""
        # Update the request first
        request = super(NurseryRequest, self).write(vals)

        # Send notifications if certain fields are modified
        notify_fields = {"request_line_ids", "state"}

        if any(field in vals for field in notify_fields):
            for record in self:
                recipients = record._get_notification_recipients()
                message_body = ("The nursing request %s has been updated by %s.") % (
                    record.name,
                    record.nurse_id.name,
                )
                record.message_post(
                    body=message_body,
                    partner_ids=recipients.mapped("partner_id").ids,
                )
        return request

    def action_approve(self):
        """Allow storekeepers to approve requests and deduct stock properly"""
        # Get the current user's employee record
        employee = self.env.user.employee_id
        if not employee:
            raise ValidationError("The current user is not linked to an employee.")

        # Permission check (do it once)
        if not self.env.user.has_group(
            "nursery_requests.group_storekeeper"
        ) and not self.env.user.has_group("nursery_requests.group_manager"):
            raise ValidationError("You do not have permission to approve requests.")

        # Stock MOVE TEST Feature [1]
        stock_picking_type = self.env.ref(
            "stock.picking_type_out"
        )  # Adjust this based on your setup
        stock_location_source = self.env.ref(
            "stock.stock_location_stock"
        )  # Warehouse stock location
        stock_location_dest = self.env.ref(
            "stock.stock_location_customers"
        )  # Destination (e.g., nurse’s station)

        for request in self:
            if request.state not in ["draft", "pending"]:
                raise ValidationError("Approved or cancelled applications cannot be upgraded to other states.")

            # Stock MOVE TEST Feature [2]
            picking_vals = {
                "picking_type_id": stock_picking_type.id,
                "location_id": stock_location_source.id,
                "location_dest_id": stock_location_dest.id,
                "origin": request.name,
                "move_type": "direct",
                "state": "draft",
            }
            picking = self.env["stock.picking"].create(picking_vals)

            stock_moves = []  # Stock MOVE TEST Feature [3]

            # Check stock availability for all lines
            exceeded_products = []  # TESTING QTY EXCEEDED

            for line in request.request_line_ids:
                product = line.product_id
                if product.qty_available < line.quantity:
                    exceeded_products.append(
                        product.name
                    )  # Adding products that exceed the stock

                # Stock MOVE TEST Feature [4]
                # Correct stock deduction: Create a Stock Move
                stock_moves.append(
                    {
                        "name": product.display_name,
                        "product_id": product.id,
                        "product_uom_qty": line.quantity,
                        "product_uom": product.uom_id.id,
                        "picking_id": picking.id,
                        "location_id": stock_location_source.id,
                        "location_dest_id": stock_location_dest.id,
                        "state": "draft",
                    }
                )

            # If any product exceeds stock, update state to pending and notify the nurse
            if exceeded_products:  # TESTING QTY EXCEEDED
                request.write(
                    {
                        "state": "pending",
                        "date_processed": "%s" % fields.Datetime.now(),
                        "storekeeper_id": employee.id,
                    }
                )
                # Notify the nurse
                if (
                    request.nurse_id
                    and request.nurse_id.user_id
                    and request.nurse_id.user_id.partner_id
                ):
                    request.message_post(
                        body=(
                            "Your request has been set to pending due to insufficient stock of these products: %s"
                            % ", ".join(exceeded_products)
                        ),
                        partner_ids=[request.nurse_id.user_id.partner_id.id],
                    )
                    _logger.info(
                        "Request %s set to pending due to insufficient stock for products: %s",
                        request.name,
                        ", ".join(exceeded_products),
                    )
                else:
                    _logger.warning(
                        "No valid partner found for nurse on request %s",
                        request.id,
                    )
                # Return a client action to display the warning
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": "Nursing Request exceed stock ⚠️",
                        "message": f"The following products exceed available stock: {', '.join(exceeded_products)}.\n"
                        f"The request has been set to pending.",
                        "type": "warning",  # Used 'warning' for a warning-style notification
                        "sticky": True,  # Make the notification sticky (user must dismiss it)
                    },
                }

            # Stock MOVE TEST Feature [5]
            # Process stock moves if there are any
            if stock_moves:
                move = self.env["stock.move"].create(stock_moves)
                move._action_confirm()  # Reserve stock
                move._action_assign()  # Assign stock

            # Validate the picking to move stock
            picking.action_confirm()
            picking.action_assign()
            picking.button_validate()

            # If no products exceed stock, approve the request (OUT of LOOP to increase performance)
            request.write(
                {
                    "state": "approved",
                    "date_processed": "%s" % fields.Datetime.now(),
                    "storekeeper_id": employee.id,
                }
            )
            # Notify the nurse
            if (
                request.nurse_id
                and request.nurse_id.user_id
                and request.nurse_id.user_id.partner_id
            ):
                request.message_post(
                    body=(
                        "Your request for product: %s has been approved."
                        % ", ".join(
                            line.product_id.name for line in request.request_line_ids
                        )
                    ),
                    partner_ids=[request.nurse_id.user_id.partner_id.id],
                )
                _logger.info(
                    "Stock deduction completed successfully for request: %s",
                    request.name,
                )
            else:
                _logger.warning(
                    "No valid partner found for nurse on request %s",
                    request.id,
                )

            # Notifying admins and storekeepers about approval
            recipients = self._get_notification_recipients()
            message_body = (
                "The request %s has been approved and stock has been deducted."
                % request.name
            )
            admin_partners = recipients.mapped("partner_id")

            if admin_partners:
                request.message_post(body=message_body, partner_ids=admin_partners.ids)

    def action_cancel(self):
        """Allow the nurse to cancel only if the request is in draft state"""
        # Get the current user's employee record
        employee = self.env.user.employee_id
        if not employee:
            raise ValidationError("The current user is not linked to an employee")
        for request in self:
            if request.nurse_id != employee:
                raise ValidationError("You can only cancel you own requests.")
            if request.state != "draft":
                raise ValidationError("You can only cancel draft requests")
            request.write(
                {
                    "state": "canceled",
                    "date_processed": "%s" % fields.Datetime.now(),
                    "storekeeper_id": employee.id,
                }
            )
        recipients = self._get_notification_recipients()
        message_body = ("Hi, I'm %s and I have canceled my nursing request: %s.") % (
            self.nurse_id.name,
            self.name,
        )
        self.message_post(
            body=message_body,
            subtype_xmlid="mail.mt_comment",
            partner_ids=recipients.mapped("partner_id").ids,  # Send notifications
        )
