/** @odoo-module **/
import { Component, onWillUpdateProps, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
console.log("alert dialog loaded");
export class AlertDialog extends Component {
  static props = {
    successMessage: {
      type: String,
      optional: true,
    },
    errorMessage: {
      type: String,
      optional: true,
    },
  };

  setup() {
    this.state = useState({
      successMessage: "",
      errorMessage: "",
    });
    onWillUpdateProps((nextProps) => this.handlePropsUpdate(nextProps));
    this.clearMessage = this.clearMessage.bind(this);
  }

  handlePropsUpdate(nextProps) {
    console.log("handlePropsUpdate", nextProps);

    if (nextProps.successMessage !== this.props.successMessage) {
      if (nextProps.successMessage) {
        console.log("successMessage changed:", nextProps.successMessage);
        this.state.successMessage = nextProps.successMessage;
      }
    }
    if (nextProps.errorMessage !== this.props.errorMessage) {
      if (nextProps.errorMessage) {
        console.log("errorMessage changed:", nextProps.errorMessage);
        this.state.errorMessage = nextProps.errorMessage;
      }
    }
  }
  clearMessage(messageType) {
    if (messageType === "success") {
      this.state.successMessage = "";
    } else if (messageType === "error") {
      this.state.errorMessage = "";
    }
    console.log(`${messageType} message cleared`);
  }
}

AlertDialog.template = "childcare_management.AlertDialogTemplate";

registry
  .category("public_components")
  .add("childcare_management.AlertDialog", AlertDialog);

export default AlertDialog;
