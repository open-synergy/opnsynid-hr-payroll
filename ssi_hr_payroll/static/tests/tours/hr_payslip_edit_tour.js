odoo.define("ssi_hr_payroll.hr_payslip_edit_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/02-edit.md
    tour.register(
        "ssi_hr_payroll_hr_payslip_edit",
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
                content: "Payslips list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Payslips)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Find and open the payslip record to edit. The
            // Pre-Condition draft record is prepared in setUpClass for employee
            // "TOUR PAYSLIP EDIT".
            {
                content: "Open the payslip",
                trigger: ".o_data_row:contains(TOUR PAYSLIP EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Payslip form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                // 14.0: an already-existing record opens readonly; Edit is
                // required before any field can be changed.
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Change the required fields.
            {
                content: "Change the Date field",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 02/01/2024",
            },

            // ── Flow 4 — On the Input Lines tab, click Reload to rebuild the
            // Input Lines list from the salary rules of the current Salary
            // Structure.
            {
                content: "Open the Input Lines tab",
                trigger: ".o_notebook .nav-link:contains(Input Lines)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click Reload on the Input Lines tab",
                trigger: "button[name='action_reload_input_lines']",
                extra_trigger: ".o_form_view.o_form_editable",
            },

            // ── Flow 5 — On the Reference tab, click Reload under Allowance
            // and under Deduction to refresh the reference move lines.
            {
                content: "Open the Reference tab",
                trigger: ".o_notebook .nav-link:contains(Reference)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click Reload under Allowance",
                trigger: "button[name='action_recompute_allowance_ref']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click Reload under Deduction",
                trigger: "button[name='action_recompute_deduction_ref']",
                extra_trigger: ".o_form_view.o_form_editable",
            },

            // ── Flow 6 — Click Compute Payslip and confirm the dialog to
            // refresh the payslip.
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

            // ── Post-Condition — The payslip record is updated with the new
            // values; the form returns to readonly mode.
            {
                content: "Payslip is saved and back to readonly mode",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
