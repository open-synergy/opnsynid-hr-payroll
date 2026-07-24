odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_approve_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/05-approve.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_approve",
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

            // ── Flow 2 — Open the batch to approve. The Pre-Condition record (in
            // Waiting for Approval, with admin as approver) is prepared in
            // setUpClass and carries the type "TOUR BATCH APPROVE".
            {
                content: "Open the batch",
                trigger: ".o_data_row:contains(TOUR BATCH APPROVE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — All approval levels are fulfilled, so status
            // changes to Done.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
