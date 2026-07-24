odoo.define(
    "ssi_hr_payroll_batch_operating_unit.hr_payslip_batch_field_ou_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_payslip_batch/01-create.md (E1 delta — Operating Unit field)
        // Backing: navigation steps come from the base ssi_hr_payroll_batch
        // 01-create Flow (open menu -> New); the delta assertion (Operating Unit
        // field is displayed) comes from this module's ## Additional Fields.
        tour.register(
            "ssi_hr_payroll_batch_operating_unit_hr_payslip_batch_field_ou",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open Human Resource > Payroll > Payslip Batches.
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
                    // Gate on the TARGET action title so the next steps do not run
                    // on the stale landing view of the app's first menu.
                    content: "Payslip Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Base Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Delta assertion — the Operating Unit field is displayed on the
                // batch form for a Multi Operating Unit user. The tour stops here;
                // it does not proceed to any base state action.
                {
                    content: "Operating Unit field is displayed on the batch form",
                    trigger: ".o_form_view .o_field_widget[name='operating_unit_id']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
