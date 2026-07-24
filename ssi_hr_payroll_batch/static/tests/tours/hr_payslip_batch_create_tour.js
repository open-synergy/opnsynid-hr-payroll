odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_create_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/01-create.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Payroll > Payslip Batches menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Payroll menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_payroll_root_menu"]',
            },
            {
                content: "Open the Payslip Batches menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll_batch.hr_payslip_batch_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Payslip Batches list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Click the New button. (14.0: "Create")
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Fill in the required fields. Type auto-fills the
            // Accounting Method and Journal (onchange). Only the fields needed to
            // save the batch in Draft are filled here.
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR BATCH CREATE",
            },
            {
                content: "Pick the type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR BATCH CREATE)",
                in_modal: false,
            },
            {
                content: "Fill in Batch Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/31/2024",
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 01/01/2024",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 01/31/2024",
            },

            // ── Flow 5 — On the Employees tab, use the Reload button to populate
            // the employees who have a salary structure assigned.
            {
                content: "Open the Employees tab",
                trigger: ".o_notebook .nav-link:contains(Employees)",
            },
            {
                content: "Click the Reload button",
                trigger: ".o_form_view button[name='action_reload_employee']",
                extra_trigger: ".o_form_view",
            },
            {
                // Reload is an object button: it auto-saves the record and writes
                // employee_ids asynchronously. Gate on the loaded employee rows so
                // the Save below does not race Reload's in-flight save (which would
                // leave the form stuck in edit mode).
                content: "Employees are loaded",
                trigger: ".o_field_widget[name='employee_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: "body:not(:has(.modal))",
            },

            // ── Post-Condition — A new Payslip Batch record is created in Draft
            // status and displayed on the form.
            {
                content: "Batch is saved and in Draft status",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
