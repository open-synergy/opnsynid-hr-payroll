odoo.define("ssi_hr_payroll.hr_employee_input_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_employee_input_type/01-create.md
    tour.register(
        "ssi_hr_payroll_hr_employee_input_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Payroll >
            // Employee Input Types menu
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
                content: "Open the Payroll > Employee Input Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_employee_input_type_menu"]',
            },
            {
                // Gate on the TARGET action title (breadcrumb) instead of a
                // generic ".o_list_view": opening the app lands on its first
                // menu, so a generic list selector would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Employee Input Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Employee Input Types)",
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

            // ── Flow 3 — Fill in the required fields (Name, Code). Active is
            // kept enabled by default and Default Amount is left on its default
            // value 0.0, so only Name and Code are filled here.
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EMPLOYEE-INPUT-TYPE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text TOUR-EIT",
            },

            // ── Flow 4 — (Optional) Write additional information in the Note
            // tab. This Flow step is optional in the work instruction and is
            // not needed to save the record, so nothing is written here.

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new Employee Input Type record is created;
            // the saved record is displayed on the form and in the breadcrumb.
            {
                content: "Employee Input Type record is saved and displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR-EMPLOYEE-INPUT-TYPE)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
