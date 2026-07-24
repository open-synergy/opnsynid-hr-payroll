odoo.define(
    "ssi_hr_payroll_batch_summary_report.hr_payslip_batch_report_buttons_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_payslip_batch/20-salary-summary-report.md
        //
        // Archetype E3 (new buttons). Per the issue's Keputusan Desain the tour
        // verifies the CONDITIONAL VISIBILITY of the two report buttons and does
        // NOT click them: clicking triggers a report download/render whose file
        // content cannot be verified through a tour (and would hang it). It only
        // asserts the buttons are present, enabled and gated by the batch state:
        //   - non-draft batch  -> both buttons visible & enabled
        //   - draft batch      -> both buttons hidden
        tour.register(
            "ssi_hr_payroll_batch_summary_report_hr_payslip_batch_report_buttons",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Flow 1 — Open the Human Resource > Payroll > Payslip Batches menu.
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
                    content: "Payslip Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 2 — Open the non-draft batch. The Pre-Condition record
                // (In Progress, with payslips) is prepared in setUpClass and
                // carries the type "TOUR SUMMARY NONDRAFT".
                {
                    content: "Open the non-draft batch",
                    trigger:
                        ".o_data_row:contains(TOUR SUMMARY NONDRAFT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Batch form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3/4 — On a non-draft batch both report buttons are visible
                // and enabled. Assert only (do not click: the click starts a report
                // download that cannot be verified by a tour and would hang it).
                {
                    content: "Salary Summary button is visible and enabled",
                    trigger:
                        ".o_statusbar_buttons button[name='action_print_salary_summary']:enabled:not(.o_invisible_modifier)",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the report download.
                    },
                },
                {
                    content: "Export XLSX button is visible and enabled",
                    trigger:
                        ".o_statusbar_buttons button[name='action_export_salary_summary_xlsx']:enabled:not(.o_invisible_modifier)",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the report download.
                    },
                },

                // ── Return to the list to inspect the draft batch.
                {
                    content: "Go back to the Payslip Batches list",
                    trigger:
                        ".o_control_panel .breadcrumb-item:not(.active):contains(Payslip Batches) a",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Payslip Batches list is displayed again",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Negative case — Open the draft batch. The Pre-Condition record
                // (still in Draft) is prepared in setUpClass and carries the type
                // "TOUR SUMMARY DRAFT".
                {
                    content: "Open the draft batch",
                    trigger:
                        ".o_data_row:contains(TOUR SUMMARY DRAFT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Draft batch form is displayed",
                    trigger:
                        ".o_form_view .o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── On a draft batch both report buttons are hidden (attrs
                // invisible adds the o_invisible_modifier / display:none). A tour
                // trigger only matches a VISIBLE element, so the hidden button
                // cannot be targeted directly; instead assert on the visible
                // statusbar-buttons container that carries NO visible instance of
                // the button (jQuery :not(:has(...:visible))).
                {
                    content: "Salary Summary button is hidden on a draft batch",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_print_salary_summary']:visible))",
                    extra_trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; the button must be present but hidden.
                    },
                },
                {
                    content: "Export XLSX button is hidden on a draft batch",
                    trigger:
                        ".o_statusbar_buttons:not(:has(button[name='action_export_salary_summary_xlsx']:visible))",
                    extra_trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; the button must be present but hidden.
                    },
                },
            ]
        );
    }
);
