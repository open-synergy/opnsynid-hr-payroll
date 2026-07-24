odoo.define("ssi_hr_payroll_timesheet.hr_payslip_tab_timesheet_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/01-create.md (E1 delta — Timesheet tab)
    //
    // Backing = base IK ∪ delta IK. The navigation flow (open menu, open the
    // record) is taken from the base IK
    // (ssi_hr_payroll/docs/hr_payslip/01-create.md); the delta assertion is the
    // Timesheet tab this module adds. The payslip is prepared in setUpClass, so
    // the tour opens that record instead of creating a new one, then asserts the
    // Timesheet tab and its field are shown. It does NOT continue to any state
    // action, and it does NOT assert timesheet row values (that is unit-test
    // territory).
    tour.register(
        "ssi_hr_payroll_timesheet_hr_payslip_tab_timesheet",
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

            // ── Base IK — Open the payslip prepared in setUpClass. The employee
            // name is the stable marker used to find the row.
            {
                content: "Open the prepared payslip",
                trigger:
                    ".o_data_row:contains(TOUR PAYSLIP TIMESHEET) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Payslip form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Delta — the Timesheet tab is present; open it.
            {
                content: "Open the Timesheet tab",
                trigger: ".o_notebook .nav-link:contains(Timesheet)",
                extra_trigger: ".o_form_view",
            },

            // ── Delta assertion (Post-Condition) — the Timesheet Computations
            // field is displayed inside the now-active Timesheet tab.
            {
                content: "Timesheet Computations field is displayed",
                trigger:
                    ".o_notebook .tab-pane.active .o_field_widget[name='timesheet_computation_ids']",
                run: function () {
                    // Assertion only; the tab and its field are visible.
                },
            },
        ]
    );
});
