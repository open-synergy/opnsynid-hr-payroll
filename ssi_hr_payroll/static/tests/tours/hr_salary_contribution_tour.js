odoo.define("ssi_hr_payroll.hr_salary_contribution_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_salary_contribution/01-create.md
    tour.register(
        "ssi_hr_payroll_hr_salary_contribution_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Payroll >
            // Salary Contributions menu.
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
                content: "Open the Payroll > Salary Contributions menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_salary_contribution_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Salary Contributions list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Salary Contributions)",
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

            // ── Flow 3 — Fill in the required fields. Only the fields needed to
            // save the record are filled: Name and Code. Partner is optional and
            // left empty, and Active stays enabled by default.
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-SALARY-CONTRIBUTION",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text TOUR-SC",
            },

            // ── Flow 4 — (Optional) Write additional information in the Note tab.
            // Not needed to save the record, so nothing is done here.

            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new Salary Contribution record is created; the
            // saved record is displayed on the form and in the breadcrumb.
            {
                content: "Salary Contribution record is saved and displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR-SALARY-CONTRIBUTION)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
