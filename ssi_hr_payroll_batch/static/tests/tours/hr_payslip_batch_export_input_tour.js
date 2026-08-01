odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_export_input_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/15-export-input.md
    //
    // This tour deliberately stops at asserting the Export Input button is
    // visible and enabled — it never clicks it. Clicking triggers an
    // ir.actions.act_url file download, which has no DOM signal a tour can
    // wait on and can hang headless Chrome. See the IK Pre-Condition/Flow
    // for the full click-flow; the downloaded file's content is unit-test
    // territory, not tour territory.
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_export_input",
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

            // ── Flow 2 — Open the batch to export payslip inputs from. The
            // Pre-Condition record (status In Progress) is prepared in
            // setUpClass and carries the type "TOUR BATCH EXPORT INPUT".
            {
                content: "Open the batch",
                trigger:
                    ".o_data_row:contains(TOUR BATCH EXPORT INPUT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — On the Payslips tab, the Export Input button is
            // visible and enabled. It is NOT clicked (see comment above).
            {
                content: "Open the Payslips tab",
                trigger: ".o_notebook .nav-link:contains(Payslips)",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Export Input button is visible and enabled",
                trigger: ".o_form_view button[name='action_export_input']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
