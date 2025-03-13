/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import AlertDialog from "../alert_dialog/alert_dialog";
console.log("Change pssword owl component loaded");
export class ChangePassword extends Component {
  static template = "childcare_management.ChangePasswordTemplate";
  static components = { AlertDialog };
  setup() {
    this.state = useState({
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
      wasValidated: false,
      isValid: {
        currentPassword: false,
        newPassword: false,
        confirmPassword: false,
        passwordsMatch: false,
      },
      passwordStrength: {
        score: 0,
        label: "Very Weak",
        color: "danger",
      },
      successMessage: "",
      errorMessage: "",
    });

    this.rpc = useService("rpc");
  }

  validateField(field, value) {
    switch (field) {
      case "currentPassword":
        this.state.isValid.currentPassword = value && value.length >= 1;
        break;
      case "newPassword":
        const hasMinLength = value && value.length >= 8;
        const hasUpperCase = /[A-Z]/.test(value);
        const hasLowerCase = /[a-z]/.test(value);
        const hasNumbers = /\d/.test(value);
        const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(value);

        // Calculate password strength
        let score = 0;
        if (hasMinLength) score++;
        if (hasUpperCase) score++;
        if (hasLowerCase) score++;
        if (hasNumbers) score++;
        if (hasSpecialChars) score++;

        // Set password strength indicators
        this.state.passwordStrength.score = score;

        if (score <= 1) {
          this.state.passwordStrength.label = "Very Weak";
          this.state.passwordStrength.color = "danger";
        } else if (score === 2) {
          this.state.passwordStrength.label = "Weak";
          this.state.passwordStrength.color = "warning";
        } else if (score === 3) {
          this.state.passwordStrength.label = "Medium";
          this.state.passwordStrength.color = "info";
        } else if (score === 4) {
          this.state.passwordStrength.label = "Strong";
          this.state.passwordStrength.color = "primary";
        } else {
          this.state.passwordStrength.label = "Very Strong";
          this.state.passwordStrength.color = "success";
        }

        this.state.isValid.newPassword = hasMinLength;

        // Check if passwords match whenever new password changes
        this.checkPasswordsMatch();
        break;
      case "confirmPassword":
        this.state.isValid.confirmPassword = value && value.length >= 8;
        this.checkPasswordsMatch();
        break;
    }
  }

  checkPasswordsMatch() {
    this.state.isValid.passwordsMatch =
      this.state.newPassword &&
      this.state.confirmPassword &&
      this.state.newPassword === this.state.confirmPassword;
  }

  onFieldChange(event, field) {
    const value = event.target.value;
    this.state[field] = value;
    this.validateField(field, value);
  }

  isFormValid() {
    return (
      this.state.isValid.currentPassword &&
      this.state.isValid.newPassword &&
      this.state.isValid.confirmPassword &&
      this.state.isValid.passwordsMatch
    );
  }

  async submitForm(event) {
    event.preventDefault();
    this.state.wasValidated = true;

    if (!this.isFormValid()) {
      this.state.errorMessage = "Please correct the errors in the form.";
      return;
    } else {
      this.state.errorMessage = "";
    }

    try {
      const result = await this.changePassword();
      if (result.success) {
        this.state.successMessage = "Password changed successfully!";
        this.state.errorMessage = "";
        this.resetForm();

        // Ocultar el mensaje después de 3 segundos
        setTimeout(() => {
          this.state.successMessage = "";
        }, 3000);
      } else {
        this.state.errorMessage = result.error || "Error changing password.";
        this.state.successMessage = "";
      }
    } catch (error) {
      console.error("Error:", error);
      this.state.errorMessage =
        "An unexpected error occurred. Please try again.";
      this.state.successMessage = "";
    }
  }

  resetForm() {
    this.state.currentPassword = "";
    this.state.newPassword = "";
    this.state.confirmPassword = "";
    this.state.wasValidated = false;
    this.state.passwordStrength.score = 0;
    this.state.passwordStrength.label = "Very Weak";
    this.state.passwordStrength.color = "danger";
  }

  async changePassword() {
    const data = {
      current_password: this.state.currentPassword,
      new_password: this.state.newPassword,
      confirm_password: this.state.confirmPassword,
    };
    return await this.rpc("/account/change_password_json", data);
  }
}

registry
  .category("public_components")
  .add("childcare_management.ChangePassword", ChangePassword);
