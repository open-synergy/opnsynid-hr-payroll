odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_import_input_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/16-import-input.md
    //
    // This tour stops at asserting the Import Input wizard opens, then
    // closes it — it never uploads a file. There is no DOM signal a tour
    // can use to attach a real file to a hidden <input type="file">
    // reliably across browsers, and doing so is unit-test territory
    // (import_payslip_batch_input.action_import is covered by a plain
    // Python test instead). See the IK Flow for the full click-flow.
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_import_input",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Payroll > Payslip
            // Batches menu.
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

            // ── Flow 2 — Open the batch to import payslip inputs into. The
            // Pre-Condition record (status In Progress) is prepared in
            // setUpClass and carries the type "TOUR BATCH IMPORT INPUT".
            {
                content: "Open the batch",
                trigger:
                    ".o_data_row:contains(TOUR BATCH IMPORT INPUT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — On the Payslips tab, click the Import Input
            // button. Its DOM name is a numeric window action id (resolved
            // from "%(hr_payslip_batch_input_import_action)d"), so it is
            // targeted by its visible label instead.
            {
                content: "Open the Payslips tab",
                trigger: ".o_notebook .nav-link:contains(Payslips)",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Click the Import Input button",
                trigger: ".o_form_view button:enabled:contains('Import Input')",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — The wizard appears. Triggers below are written
            // relative to the modal content, never prefixed with ".modal"
            // (14.0 scopes in-modal triggers via
            // $modal_displayed.find(trigger); see the cancel tour).
            {
                content: "The Import Payslip Batch Input wizard is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Post-Condition (partial, by design) — close the wizard
            // without uploading a file; file upload is out of scope for
            // this tour (see comment above).
            {
                content: "Discard the wizard",
                trigger: ".modal-footer button.btn-secondary",
            },
            {
                content: "Wizard is closed",
                trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
