odoo.define("ssi_hr_payroll_batch.hr_payslip_batch_print_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip_batch/18-print.md
    //
    // Boundary (patterns.md §Q): this tour only proves the button opens the
    // "Select Report To Print" wizard, then closes it via Cancel. It never
    // selects a report nor clicks the wizard's own Print button, because the
    // resulting report action is an ir.actions.act_url download with no DOM
    // "finished" signal — clicking through it could hang headless Chrome.
    tour.register(
        "ssi_hr_payroll_batch_hr_payslip_batch_print",
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

            // ── Flow 2 — Open the batch to print. The Pre-Condition record
            // is prepared in setUpClass and carries the type "TOUR BATCH
            // PRINT"; it is left in Draft, since the Print button is not
            // guarded by any state condition.
            {
                content: "Open the batch",
                trigger: ".o_data_row:contains(TOUR BATCH PRINT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Batch form is displayed",
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
            // the batch form is displayed again. Whether a report is
            // actually generated and downloaded is out of tour scope.
            {
                content: "Wizard is closed and the batch form is displayed",
                trigger: ".o_form_view",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
