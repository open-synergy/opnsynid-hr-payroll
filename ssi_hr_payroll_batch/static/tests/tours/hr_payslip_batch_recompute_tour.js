odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_recompute_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/14-recompute.md
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_recompute",
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

            // ── Flow 2 — Open the batch to recompute. The Pre-Condition record
            // (status In Progress, one draft payslip) is prepared in setUpClass
            // and carries the type "TOUR BATCH RECOMPUTE".
            {
                content: "Open the batch",
                trigger:
                    ".o_data_row:contains(TOUR BATCH RECOMPUTE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — On the Payslips tab, click the Re-Compute button.
            {
                content: "Open the Payslips tab",
                trigger: ".o_notebook .nav-link:contains(Payslips)",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Click the Re-Compute button",
                trigger: ".o_form_view button[name='action_compute_payslip']",
                extra_trigger: ".o_form_view",
            },

            // ── Post-Condition — Every draft payslip has its salary rules
            // recomputed; the batch stays on the same form, still In Progress.
            {
                content: "Batch form is still rendered, still In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                extra_trigger: ".o_form_view button[name='action_compute_payslip']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
