odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_start_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/07-start.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_start",
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

            // ── Flow 2 — Open the batch to start. The Pre-Condition draft record
            // (with employees) is prepared in setUpClass and carries the type
            // "TOUR BATCH START", shown in the Type column of the list.
            {
                content: "Open the batch",
                trigger: ".o_data_row:contains(TOUR BATCH START) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Start button. It is an action-mixin button;
            // target it by its visible label rather than its DOM name.
            {
                content: "Click the Start button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Start)",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to In Progress.
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
