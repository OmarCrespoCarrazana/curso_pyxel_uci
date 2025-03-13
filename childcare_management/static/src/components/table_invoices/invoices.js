/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { GenericTable } from "../geneic_table/generic_table/generic_table";

export class InvoicesTable extends Component {
  static template = "childcare_management.InvoicesTableTemplate";
  static components = { GenericTable };

  setup() {
    this.orm = useService("orm");

    this.state = useState({
      records: [],
      filteredData: [],
      filters: {
        global: "",
        payment_state: "",
        amount_total: "",
        invoice_date_due: "",
      },
      isLoading: false,
    });

    this.columns = [
      {
        name: "name",
        header: "Number",
        isSortable: true,
        cell: (value) => markup(`<span class="text-primary">${value}</span>`),
      },
      {
        name: "invoice_date",
        header: "Created On",
        isSortable: true,
        cell: (value) => (value ? new Date(value).toLocaleDateString() : "-"),
      },
      {
        name: "invoice_date_due",
        header: "Due Date",
        cell: (value, row) => this.formatDueDate(value, row),
      },
      {
        name: "amount_tax",
        header: "Taxes",
        isSortable: true,
        cell: (value, row) => this.formatCurrency(value),
      },
      {
        name: "amount_total",
        header: "Total",
        cell: (value, row) => this.formatCurrency(value),
      },
      {
        name: "currency_id",
        header: "Currency",
        cell: (value) => value[1],
      },
      {
        name: "payment_state",
        header: "Status",
        cell: (value, row) => this.renderPaymentStatus(value, row),
      },
      // {
      //   name: "actions",
      //   header: "Actions",
      //   cell: (_, row) => this.renderActions(row),
      // },
    ];

    this._loadInvoices();
    this.updateFilter = this.updateFilter.bind(this);
  }

  async _loadInvoices() {
    this.state.isLoading = true;
    try {
      const invoicesData = await this.orm.searchRead(
        "account.move",
        [
          ["move_type", "=", "out_invoice"],
          ["state", "=", "posted"],
        ],
        [
          "name",
          "partner_id",
          "invoice_date",
          "invoice_date_due",
          "amount_tax",
          "amount_total",
          "currency_id",
          "payment_state",
        ],
        { order: "invoice_date desc" }
      );

      console.log("Datos reales:", invoicesData);

      this.state.records = invoicesData.map((invoice) => ({
        ...invoice,
      }));
      this.state.filteredData = [...this.state.records];
    } catch (error) {
      console.error("Error cargando facturas:", error);
    } finally {
      this.state.isLoading = false;
    }
  }

  formatCurrency(value) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(value);
  }

  formatDueDate(dateString, row) {
    if (!dateString) return "-";

    const dueDate = new Date(dateString);
    const today = new Date();
    const diffDays = Math.floor((dueDate - today) / (1000 * 60 * 60 * 24));

    let statusClass = "";
    let text = new Date(dateString).toLocaleDateString();

    if (row.payment_state === "paid") {
      return text;
    }

    if (diffDays === 0) {
      statusClass = "text-warning";
      text = "Today";
    } else if (diffDays < 0) {
      statusClass = "text-danger";
      text = `${Math.abs(diffDays)} days ago`;
    }

    return markup(`<span class="${statusClass}">${text}</span>`);
  }

  renderPaymentStatus(value, row) {
    const statusMap = {
      paid: { label: "Paid", class: "success" },
      not_paid: { label: "Not Paid", class: "danger" },
      in_payment: { label: "In Payment", class: "warning" },
    };

    const status = statusMap[value.toLowerCase()] || {
      label: value,
      class: "secondary",
    };
    return markup(
      `<span class="badge bg-${status.class}">${status.label}</span>`
    );
  }
  renderActions(row) {
    return markup(
      `<i class="fa fa-eye text-secondary action-view" data-id="${row.id}"></i>`
    );
  }

  updateFilter(filterType, value) {
    this.state.filters[filterType] = value;
    this.applyFilters();
  }
  applyFilters() {
    this.state.filteredData = this.state.records.filter((record) => {
      return Object.entries(this.state.filters).every(([key, filterValue]) => {
        if (!filterValue) return true;
        // Filtro global
        if (key === "global") {
          return this.columns.some((col) =>
            String(record[col.name])
              .toLowerCase()
              .includes(filterValue.toLowerCase())
          );
        }

        if (key === "payment_state") {
          const cellValue = String(record.payment_state || "").toLowerCase();
          return cellValue === filterValue.toLowerCase();
        }

        if (key === "amount_total") {
          const numericValue = parseFloat(record.amount_total || 0);
          const numericFilter = parseFloat(filterValue);
          return !isNaN(numericFilter) && numericValue >= numericFilter;
        }

        if (key === "invoice_date_due") {
          if (!filterValue) return true;
          const recordDate = new Date(record.invoice_date_due)
            .toISOString()
            .split("T")[0];
          return recordDate === filterValue;
        }
      });
    });
    console.log("Filtered Data:", this.state.filteredData);
  }
  // Then handle the click event at the parent level
  onActionClicked(event) {
    // Check if the clicked element or its parent is the view button
    const button = event.target.closest(".action-view");
    if (button) {
      const invoiceId = button.dataset.id;
      console.log("View action clicked for invoice:", invoiceId);
      // Handle the view action here
    }
  }
}

registry
  .category("public_components")
  .add("childcare_management.InvoicesTable", InvoicesTable);
