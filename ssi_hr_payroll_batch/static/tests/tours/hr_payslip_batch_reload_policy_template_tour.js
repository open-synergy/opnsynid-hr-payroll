odoo.define(
    "ssi_hr_payroll_batch.hr_payslip_batch_reload_policy_template_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_payslip_batch/19-reload-policy-template.md
        tour.register(
            "ssi_hr_payroll_batch_hr_payslip_batch_reload_policy_template",
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

                // ── Flow 2 — Open the batch whose policy template needs to
                // be reloaded. The Pre-Condition record (any status, admin
                // is a member of `base.group_system` by default) is
                // prepared in setUpClass for type "TOUR BATCH RELOAD
                // POLICY".
                {
                    content: "Open the batch",
                    trigger:
                        ".o_data_row:contains(TOUR BATCH RELOAD POLICY) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Batch form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — Open the Policies tab.
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content:
                        "The Reload Template Policy button is displayed and enabled",
                    trigger:
                        ".o_form_view button[name='action_reload_policy_template']",
                    extra_trigger: ".o_notebook .nav-link.active:contains(Policies)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 4 — Click the Reload Template Policy button.
                {
                    content: "Click the Reload Template Policy button",
                    trigger:
                        ".o_form_view button[name='action_reload_policy_template']",
                },

                // ── Post-Condition — the Policies tab remains displayed and
                // no error dialog was raised. The resulting
                // `policy_template_id` value (and the dependent `*_ok`
                // fields it recomputes) is out of tour scope — see the
                // Boundary note in the docstring and
                // 19-reload-policy-template.md; that is unit test
                // territory.
                {
                    content:
                        "The Policies tab is still displayed, with no error raised",
                    trigger: ".o_notebook .nav-link.active:contains(Policies)",
                    extra_trigger:
                        "body:not(:has(.modal)) .o_form_view button[name='action_reload_policy_template']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
