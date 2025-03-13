/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import AlertDialog from "../alert_dialog/alert_dialog";

export class ChildRegistration extends Component {
  static template = "childcare_management.ChildRegistrationTemplate";
  static components = { AlertDialog };
  setup() {
    this.state = useState({
      isModalOpen: false,
      name: "",
      idNumber: "",
      nameValid: false,
      idNumberValid: false,
      wasValidated: false,
      errorMessage: "",
    });
    this.rpc = useService("rpc");
  }

  openModal() {
    this.state.isModalOpen = true;
  }

  closeModal() {
    this.state.isModalOpen = false;
    this.resetForm();
  }

  resetForm() {
    this.state.name = "";
    this.state.idNumber = "";
    this.state.nameValid = false;
    this.state.idNumberValid = false;
    this.state.wasValidated = false;
  }

  validateName(name) {
    const regex = /^[A-Za-záéíóúñÁÉÍÓÚÑ\s]+$/;
    return regex.test(name) && name.length >= 2;
  }

  validateIdNumber(idNumber) {
    const regex = /^\d{11}$/;
    if (!regex.test(idNumber)) return false;

    // Validación de fecha (año/mes/día)
    const year = parseInt(idNumber.substring(0, 2));
    const month = parseInt(idNumber.substring(2, 4));
    const day = parseInt(idNumber.substring(4, 6));

    if (month < 1 || month > 12) return false;
    if (day < 1 || day > 31) return false;

    return true;
  }

  onNameChange(event) {
    const value = event.target.value;
    this.state.name = value;
    this.state.nameValid = this.validateName(value);
    this.state.nameError = "";
  }

  onIdNumberChange(event) {
    const value = event.target.value;
    this.state.idNumber = value.replace(/\D/g, "");
    this.state.idNumberValid = this.validateIdNumber(this.state.idNumber);
  }

  async submitForm(event) {
    event.preventDefault();
    this.state.wasValidated = true;

    if (!this.state.nameValid || !this.state.idNumberValid) {
      return;
    }

    try {
      console.log("Enviando formulario válido:", {
        name: this.state.name,
        idNumber: this.state.idNumber,
      });

      const result = await this.registerChild();
      console.log("Resultado del envío", result);
      this.closeModal();
    } catch (error) {
      // Procesamos el error para extraer el mensaje
      let errorMsg = "Ocurrió un error";
      if (error.data && error.data.message) {
        errorMsg = error.data.message;
      } else if (error.message) {
        errorMsg = error.message;
      }

      this.state.successMessage = "";
      this.state.errorMessage = "";
      console.log(
        "mensaje limpiado antes de colocarlo de nuevo",
        this.state.errorMessage
      );
      setTimeout(() => {
        this.state.errorMessage = errorMsg;
      }, 0);

      console.error("Error capturado:", errorMsg);
    }
  }

  async registerChild() {
    const data = {
      name: this.state.name,
      id_number: this.state.idNumber,
    };

    const result = await this.rpc("/request-service", data);
    // Si el RPC devuelve un error, lo lanzamos para capturarlo en submitForm
    console.log("Resultado del rpc", result);
    if (result.status===200){
      return result;
    }
    if (result.status === 400 || 500) {
      throw result;
    }
    
  }
}

registry
  .category("public_components")
  .add("childcare_management.ChildRegistration", ChildRegistration);
