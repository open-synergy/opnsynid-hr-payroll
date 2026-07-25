odoo.define("ssi_hr_payroll.hr_payslip_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_type/01-create.md
    tour.register(
        "ssi_hr_payroll_hr_payslip_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Payroll >
            // Types menu
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Payroll > Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_payslip_type_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Payslip Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Payslip Types)",
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

            // ── Flow 3 — Fill in the required fields (Name, Code, Accounting
            // Method). Accounting Method is left on its default value
            // "Journal at Payslip".
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-PAYSLIP-TYPE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text TOUR-PST",
            },

            // ── Flow 4 — (Optional) Fill in the accounting configuration
            // fields (Journal, Analytic Account, Debit Usage, Credit Usage).
            // This Flow step is optional in the work instruction and is not
            // needed to save the record, so no field is filled here.

            // ── Flow 5 — (Optional) Configure the M2O configurator. Open the
            // Employee Configurator tab and switch Selection Method to
            // "Manual".
            {
                content: "Open the Employee Configurator tab",
                trigger: ".o_notebook .nav-link:contains(Employee Configurator)",
            },
            {
                content: "Employee Configurator tab is displayed",
                trigger: ".o_field_widget[name='employee_selection_method']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Switch Employee Selection Method to Manual",
                trigger: ".o_field_widget[name='employee_selection_method'] select",
                run: "text Manual",
            },
            {
                content: "Employees field becomes visible for the Manual method",
                trigger: ".o_field_widget[name='employee_ids']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 6 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new Payslip Type record is created; the
            // saved record is displayed on the form and in the breadcrumb,
            // and the M2O configurator choice made in Flow 5 was persisted.
            {
                content: "Payslip Type record is saved and displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR-PAYSLIP-TYPE)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Employee Selection Method was saved as Manual",
                trigger:
                    ".o_field_widget[name='employee_selection_method']:contains(Manual)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
