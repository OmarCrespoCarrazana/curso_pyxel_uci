/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { GenericTable } from "../geneic_table/generic_table/generic_table";

export class MedicalRecordsTable extends Component {
  static template = "childcare_management.MedicalRecordsTableTemplate";
  static components = { GenericTable };
  static props = {
    child_id: Number,
  };
  setup() {
    this.orm = useService("orm");
    this.rpc = useService("rpc");
    this.state = useState({
      child: null,
      doctor: null,
      vaccines: null,
      last_updated: null,
      records: [],
      isLoading: true,
    });

    this.columns = [
      {
        name: "id",
        header: "ID",
      },
      {
        name: "date",
        header: "Date",
        cell: (value) => new Date(value).toLocaleDateString(),
      },
      {
        name: "name",
        header: "Medical Event",
      },
      {
        name: "description",
        header: "Description",
        cell: (value) => markup(value) || "-",
      },
    ];

    this.loadRecords();
  }

  async loadRecords() {
    try {
      let childId = this.props.child_id;
      console.log("childId", childId);
      if (!childId) {
        // Fallback: extraer el id desde la URL
        const urlParts = window.location.pathname.split("/");
        // Se asume que el id es el último segmento de la URL
        childId = parseInt(urlParts[urlParts.length - 1], 10);
        console.log("ChildID por url", childId);
      }

      const result = await this.rpc("/medical-records_json", {
        child_id: childId,
      });
      console.log("Medical records from backend:", result);

      if (result && result.records.length > 0) {
        this.state.child = result.records[0].child;
        this.state.doctor = result.records[0].doctor;
        this.state.vaccines = result.records[0].vaccines;
        this.state.last_updated = result.records[0].date;
        this.state.records = result.records[0].medical_events.map((event) => ({
          ...event,
          description: markup(event.description),
        }));
        this.state.isLoading = false;
      } else {
        this.state.isLoading = false;
        this.state.records = [];
      }
    } catch (error) {
      console.error("Error loading medical records:", error);
      this.state.records = [];
    }
  }

  useMarkup(value) {
    return markup(value);
  }
}

registry
  .category("public_components")
  .add("childcare_management.MedicalRecordsTable", MedicalRecordsTable);
