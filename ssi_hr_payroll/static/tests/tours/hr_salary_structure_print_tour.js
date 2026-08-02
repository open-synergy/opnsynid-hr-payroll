odoo.define("ssi_hr_payroll.hr_salary_structure_print_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_salary_structure/06-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens the
    // "Select Report To Print" wizard, then closes it via Cancel. It never
    // selects a report nor clicks the wizard's own Print button, because the
    // resulting report action is an ir.actions.act_url download with no DOM
    // "finished" signal — clicking through it could hang headless Chrome.
    tour.register(
        "ssi_hr_payroll_hr_salary_structure_print",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Payroll >
            // Salary Structures menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Payroll > Salary Structures menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_salary_structure_menu"]',
            },
            {
                content: "Salary Structures list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Salary Structures)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Open the salary structure record to print.
            {
                content: "Open the salary structure record",
                trigger:
                    ".o_data_row:contains(TOUR PRINT SALARY STRUCTURE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Salary structure form is displayed",
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

            // ── Flow 4/5 boundary — the wizard is proven open, then closed.
            // Selecting the report and clicking the wizard's own Print button
            // are intentionally NOT executed — see the module docstring above.
            //
            // 14.0: do NOT prefix the trigger with ".modal" — when a modal is
            // displayed, web_tour scopes the search to
            // $modal_displayed.find(trigger), and $modal_displayed already
            // IS the ".modal" element, so ".modal .modal-title" would look
            // for a nested modal that does not exist (patterns.md §H box).
            {
                content: "The Select Report To Print wizard is displayed",
                trigger: ".modal-title:contains('Select Report To Print')",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Close the wizard",
                // The button is declared with class="oe_link" in the wizard
                // XML, but the form renderer maps it to "btn btn-link" in
                // the DOM — the "special" attribute survives that mapping
                // and is the stable anchor.
                trigger: ".modal-footer button[special='cancel']",
                in_modal: true,
            },

            // ── Post-Condition (tour boundary) — the wizard is closed and
            // the salary structure form is displayed again. Whether a report is
            // actually generated and downloaded is out of tour scope.
            {
                content: "Wizard is closed and the salary structure form is displayed",
                trigger: ".o_form_view",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
