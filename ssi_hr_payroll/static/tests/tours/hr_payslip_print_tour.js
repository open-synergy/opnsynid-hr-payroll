odoo.define("ssi_hr_payroll.hr_payslip_print_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/15-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens the
    // "Select Report To Print" wizard, then closes it via Cancel. It never
    // selects a report nor clicks the wizard's own Print button, because the
    // resulting report action is an ir.actions.act_url download with no DOM
    // "finished" signal — clicking through it could hang headless Chrome.
    tour.register(
        "ssi_hr_payroll_hr_payslip_print",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Payroll > Payslips menu.
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
                content: "Payslips list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Payslips)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Open the payslip to print.
            {
                content: "Open the payslip",
                trigger: ".o_data_row:contains(TOUR PAYSLIP PRINT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Payslip form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Print button.
            // The button is injected by ssi_print_mixin as type="action" —
            // its ``name`` attribute is a numeric action id resolved at
            // render time, so it must be targeted by its visible label
            // (selectors.md §4), not by ``[name=...]``.
            {
                content: "Click the Print button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Print')",
                extra_trigger: ".o_form_view",
            },

            // ── Boundary — the wizard is proven open, then closed. Flow 4
            // (select the report) and Flow 5 (click the wizard's Print
            // button) are intentionally NOT executed — see the module
            // docstring above.
            {
                content: "The Select Report To Print wizard is displayed",
                trigger: ".modal .modal-title:contains('Select Report To Print')",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Close the wizard",
                trigger: ".modal-footer button.oe_link:contains('Cancel')",
                in_modal: true,
            },

            // ── Post-Condition (tour boundary) — the wizard is closed and
            // the payslip form is displayed again. Whether a report is
            // actually generated and downloaded is out of tour scope.
            {
                content: "Wizard is closed and the payslip form is displayed",
                trigger: ".o_form_view",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
