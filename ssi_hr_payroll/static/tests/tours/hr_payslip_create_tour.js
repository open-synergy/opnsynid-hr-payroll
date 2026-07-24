odoo.define("ssi_hr_payroll.hr_payslip_create_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/01-create.md
    tour.register(
        "ssi_hr_payroll_hr_payslip_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Payroll > Payslips menu.
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
                content: "Open the Payslips menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_payslip_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Payslips list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Payslips)",
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

            // ── Flow 3 — Fill in the required fields. Employee auto-fills the
            // Department/Manager/Job Position and (via onchange) the Salary
            // Structure; Type auto-fills the Journal. Only the fields needed to
            // compute and save the payslip are filled here.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR PAYSLIP CREATE",
            },
            {
                content: "Pick the employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR PAYSLIP CREATE)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/01/2024",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 01/31/2024",
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/31/2024",
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR PAYSLIP TYPE",
            },
            {
                content: "Pick the type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR PAYSLIP TYPE)",
                in_modal: false,
            },

            // ── Flow 4/5 — (Optional) Input Lines and Reference tabs. Not needed
            // to compute and save the payslip, so nothing is done here.

            // ── Flow 6 — Click Compute Payslip and confirm the dialog to compute
            // the payslip lines.
            {
                content: "Click Compute Payslip",
                trigger: ".o_statusbar_buttons button[name='action_compute_payslip']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the Compute Payslip dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Flow 7 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: "body:not(:has(.modal))",
            },

            // ── Post-Condition — A new payslip record is created in Draft status
            // and displayed on the form.
            {
                content: "Payslip is saved and in Draft status",
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
