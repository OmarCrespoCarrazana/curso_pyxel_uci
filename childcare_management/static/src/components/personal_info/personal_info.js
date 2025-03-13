/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import AlertDialog from "../alert_dialog/alert_dialog";
console.log("Personal info owl component loaded");
export class PersonalInfo extends Component {
  static template = "childcare_management.PersonalInfoTemplate";
  static components = { AlertDialog };
  setup() {
    this.state = useState({
      name: "",
      email: "",
      phone: "",
      street: "",
      street2: "",
      city: "",
      zip: "",
      country_id: "",
      state_id: "",
      countries: [],
      states: [],
      filteredStates: [],
      wasValidated: false,
      isValid: {
        name: false,
        email: false,
        phone: true,
        zip: true,
        street: false,
      },
      successMessage: "",
      errorMessage: "",
    });

    this.rpc = useService("rpc");
    this.orm = useService("orm");

    onWillStart(async () => {
      await this.loadUserData();
      await this.loadCountries();
    });
  }

  async loadUserData() {
    try {
      const userData = await this.rpc("/account/get_user_data");
      this.state.name = userData.name || "";
      this.state.email = userData.email || "";
      this.state.phone = userData.phone || "";
      this.state.street = userData.street || "";
      this.state.street2 = userData.street2 || "";
      this.state.city = userData.city || "";
      this.state.zip = userData.zip || "";
      this.state.country_id = userData.country_id || "";
      this.state.state_id = userData.state_id || "";

      // Validar campos iniciales
      this.validateField("name", this.state.name);
      this.validateField("email", this.state.email);
      this.validateField("street", this.state.street);

      if (this.state.country_id) {
        await this.loadStates(this.state.country_id);
      }
    } catch (error) {
      console.error("Error loading user data:", error);
      this.state.errorMessage = "Error loading user data. Please try again.";
    }
  }

  async loadCountries() {
    try {
      const countries = await this.orm.searchRead(
        "res.country",
        [],
        ["id", "name"],
        { order: "name" }
      );
      this.state.countries = countries;
    } catch (error) {
      console.error("Error loading countries:", error);
    }
  }

  async loadStates(countryId) {
    try {
      const states = await this.orm.searchRead(
        "res.country.state",
        [["country_id", "=", parseInt(countryId)]],
        ["id", "name"],
        { order: "name" }
      );
      this.state.filteredStates = states;
    } catch (error) {
      console.error("Error loading states:", error);
    }
  }

  validateField(field, value) {
    switch (field) {
      case "name":
        this.state.isValid.name = value && value.trim().length >= 2;
        break;
      case "email":
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        this.state.isValid.email = emailRegex.test(value);
        break;
      case "phone":
        // Opcional, pero si se proporciona debe ser válido
        if (!value) {
          this.state.isValid.phone = true;
        } else {
          const phoneRegex =
            /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
          this.state.isValid.phone = phoneRegex.test(value);
        }
        break;
      case "street":
        this.state.isValid.street = value && value.trim().length >= 3;
        break;
      case "zip":
        const regex = /^[0-9]{1,10}$/;
        this.state.isValid.zip = regex.test(value);
        break;
    }
  }

  onFieldChange(event, field) {
    const value = event.target.value;
    this.state[field] = value;
    this.validateField(field, value);

    // Si cambia el país, cargar los estados correspondientes
    if (field === "country_id" && value) {
      this.loadStates(value);
      this.state.state_id = ""; // Resetear el estado
    }
  }

  isFormValid() {
    return (
      this.state.isValid.name &&
      this.state.isValid.email &&
      this.state.isValid.phone &&
      this.state.isValid.street
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
      const result = await this.updateProfile();
      if (result.success) {
        this.state.successMessage = "Profile updated successfully!";
        this.state.errorMessage = "";

        // Ocultar el mensaje después de 3 segundos
        setTimeout(() => {
          this.state.successMessage = "";
        }, 3000);
      } else {
        this.state.errorMessage = result.error || "Error updating profile.";
        this.state.successMessage = "";
      }
    } catch (error) {
      console.error("Error:", error);
      this.state.errorMessage =
        "An unexpected error occurred. Please try again.";
      this.state.successMessage = "";
    }
  }

  async updateProfile() {
    const data = {
      name: this.state.name,
      email: this.state.email,
      phone: this.state.phone,
      street: this.state.street,
      street2: this.state.street2,
      city: this.state.city,
      zip: this.state.zip,
      country_id: this.state.country_id,
      state_id: this.state.state_id,
    };
    return await this.rpc("/account/update_profile_json", data);
  }
}

registry
  .category("public_components")
  .add("childcare_management.PersonalInfo", PersonalInfo);
