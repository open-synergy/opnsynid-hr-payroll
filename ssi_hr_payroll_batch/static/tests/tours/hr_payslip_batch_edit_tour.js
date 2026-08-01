odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_edit_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/02-edit.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_edit",
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
                content: "Payslip Batches list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Find and open the record to edit. The Pre-Condition
            // draft record is prepared in setUpClass and carries the type
            // "TOUR BATCH EDIT", shown in the Type column of the list.
            {
                content: "Open the batch",
                trigger: ".o_data_row:contains(TOUR BATCH EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
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
                content: "Change the Batch Date field",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 02/01/2024",
            },

            // ── Flow 4 — On the Employees tab, click Reload to replace
            // Employees with every employee currently allowed by the type's
            // filter, discarding manual changes on the tab.
            {
                content: "Open the Employees tab",
                trigger: ".o_notebook .nav-link:contains(Employees)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click the Reload button",
                trigger: ".o_form_view button[name='action_reload_employee']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                // Reload is an object button: it auto-saves the record and writes
                // employee_ids asynchronously. The batch already carries its own
                // employee before Reload runs, so gating on "a row exists" matches
                // instantly and lets Save race Reload's in-flight write. Gate
                // instead on an employee that can only appear AFTER
                // allowed_employee_ids (every employee with a salary structure)
                // replaces employee_ids — "TOUR BATCH CREATE EMP" belongs to a
                // different batch's type and is never part of this one on its own.
                content: "Employees are loaded",
                trigger:
                    ".o_field_widget[name='employee_ids'] .o_data_row:contains(TOUR BATCH CREATE EMP)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: "body:not(:has(.modal))",
            },

            // ── Post-Condition — The Payslip Batch record is updated with the
            // new values; the form returns to readonly mode.
            {
                content: "Batch is saved and back to readonly mode",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
