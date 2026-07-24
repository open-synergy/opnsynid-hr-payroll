odoo.define(
    "ssi_hr_payroll_batch_work_log.hr_payslip_batch_tab_work_log_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_payslip_batch/01-create.md (E1 delta — Work Log tab)
        tour.register(
            "ssi_hr_payroll_batch_work_log_hr_payslip_batch_tab_work_log",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open the Human Resource > Payroll > Payslip
                // Batches menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
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
                    // Gate on the TARGET action title: opening the app lands on its
                    // first menu, so a generic ".o_list_view" would match the stale
                    // landing view and let the next steps run on the wrong screen.
                    content: "Payslip Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Base Flow 2 — Open the payslip batch. The draft batch is prepared
                // in setUpClass tagged by the "TOUR BATCH WORK LOG" payslip type shown
                // in the Type column.
                {
                    content: "Open the payslip batch",
                    trigger:
                        ".o_data_row:contains(TOUR BATCH WORK LOG) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Payslip batch form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Delta assertion — the Work Log tab is added to the payslip batch
                // form by ssi_hr_payroll_batch_work_log. Assert the tab is present,
                // open it, and assert it becomes the active page.
                {
                    content: "The Work Log tab is displayed on the payslip batch form",
                    trigger: ".o_notebook .nav-link:contains(Work Log)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The Work Log tab is active",
                    trigger: ".o_notebook .nav-link.active:contains(Work Log)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
