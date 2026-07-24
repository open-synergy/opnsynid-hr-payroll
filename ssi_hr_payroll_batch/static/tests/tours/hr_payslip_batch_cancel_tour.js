odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_cancel_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/10-cancel.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_cancel",
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

            // ── Flow 2 — Open the batch to cancel. The Pre-Condition record is
            // prepared in setUpClass and carries the type "TOUR BATCH CANCEL".
            {
                content: "Open the batch",
                trigger: ".o_data_row:contains(TOUR BATCH CANCEL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Cancel button. It is an action button whose
            // DOM name is a numeric action id, so it is targeted by its label.
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Cancel)",
                extra_trigger: ".o_form_view",
            },
            {
                // When a modal is open the tour scopes triggers INSIDE it
                // (tour_manager.js: $modal_displayed.find(trigger)), so triggers
                // here are written relative to the wizard modal — never prefixed
                // with ".modal".
                content: "The cancellation reason wizard is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 4 — Select the Cancellation Reason (radio widget). The
            // reason is prepared in setUpClass as a global-use cancel reason.
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item label:contains(TOUR CANCEL REASON)",
            },

            // ── Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // ── Flow 6 — Click OK on the confirmation dialog. Clicking the wizard
            // Confirm (confirm="Are you sure?") opens a second modal on top; the
            // tour scopes to that topmost modal, so the trigger is relative to it.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
            },

            // ── Post-Condition — Status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
