odoo.define("ssi_hr_payroll_work_log.hr_payslip_tab_work_log_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/01-create.md (E1 delta — Work Log tab)
    tour.register(
        "ssi_hr_payroll_work_log_hr_payslip_tab_work_log",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Base Flow 1 — Open the Human Resource > Payroll > Payslips menu.
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
                content: "Open the Payslips menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_payslip_menu"]',
            },
            {
                // Gate on the TARGET action title: opening the app lands on its
                // first menu, so a generic ".o_list_view" would match the stale
                // landing view and let the next steps run on the wrong screen.
                content: "Payslips list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Payslips)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Base Flow 2 — Open the payslip. The draft record is prepared in
            // setUpClass for employee "TOUR PAYSLIP WORK LOG".
            {
                content: "Open the payslip",
                trigger:
                    ".o_data_row:contains(TOUR PAYSLIP WORK LOG) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Payslip form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Delta assertion — the Work Log tab is added to the payslip form
            // by ssi_hr_payroll_work_log. Assert the tab is present, open it, and
            // assert it becomes the active page.
            {
                content: "The Work Log tab is displayed on the payslip form",
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
});
