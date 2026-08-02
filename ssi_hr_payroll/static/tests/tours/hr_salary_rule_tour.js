odoo.define("ssi_hr_payroll.hr_salary_rule_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_salary_rule/01-create.md
    tour.register(
        "ssi_hr_payroll_hr_salary_rule_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Payroll >
            // Salary Rules menu.
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
                content: "Open the Payroll > Salary Rules menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_salary_rule_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Salary Rules list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Salary Rules)",
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

            // ── Flow 3 — Fill in the header fields. Only the fields needed to
            // save the record are filled: Name, Code, and Category (mandatory).
            // Sequence keeps its default of 5; Active stays enabled; Parent,
            // Product, and Appear on Payslip are optional and left empty.
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-SALARY-RULE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },
            {
                content: "Select the Category",
                trigger: ".o_field_many2one[name='category_id'] input",
                run: "text TOUR-CATEGORY-FOR-RULE",
            },
            {
                content: "Pick the Category from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-CATEGORY-FOR-RULE)",
                in_modal: false,
            },

            // ── Flow 4 — (Optional) Click Generate Code to have the system
            // assign a code from the configured sequence template. Code was
            // left as "/" above so the button actually replaces it; typing a
            // real code instead would leave it untouched (see
            // docs/hr_salary_rule/01-create.md).
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                // The record has no id until this button auto-saves it; the
                // breadcrumb literal "New" going away is the data-independent
                // proof the save + reload completed
                // (odoo-development-ui-test patterns.md §P). The generated
                // Code value itself is not asserted — that is a value check,
                // out of scope for a tour (odoo-development-ui-test §2).
                content: "Record is saved by Generate Code",
                trigger: ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 5 — (Optional) Fill in the General tab. Python Condition
            // and Computation are pre-filled with default expressions, and
            // Salary Contribution is optional, so nothing is done here.

            // ── Flow 6 — (Optional) Fill in the Accounting tab. Not needed to
            // save the record, so nothing is done here.

            // ── Flow 7 — (Optional) Fill in the Input Types tab. Not needed to
            // save the record, so nothing is done here.

            // ── Flow 8 — (Optional) Review the Children tab. It is filled
            // automatically when another salary rule selects this record as its
            // Parent, so nothing is done here.

            // ── Flow 9 — (Optional) Write additional information in the Note
            // tab. Not needed to save the record, so nothing is done here.

            // ── Flow 10 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new Salary Rule record is created; the saved
            // record is displayed on the form and in the breadcrumb.
            {
                content: "Salary Rule record is saved and displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR-SALARY-RULE)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
