odoo.define("ssi_hr_payroll_operating_unit.hr_payslip_field_ou_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/01-create.md (E1 delta — Additional Fields)
    // Navigation (open menu -> New) is taken from the base IK
    // ssi_hr_payroll/docs/hr_payslip/01-create.md Flow steps 1-2. The delta
    // assertion is that the Operating Unit field is visible on the form for a
    // user in the operating_unit.group_multi_operating_unit group. The tour
    // stops there; it does not fill, compute, save or confirm (E1 delta-only).
    tour.register(
        "ssi_hr_payroll_operating_unit_hr_payslip_field_ou",
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
                // Gate on the TARGET action title so the next step does not run
                // against the stale landing view of the app.
                content: "Payslips list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Payslips)",
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

            // ── Delta assertion — the Operating Unit field is visible on the
            // create form for a user in the multi operating unit group.
            {
                content: "Operating Unit field is visible on the form",
                trigger:
                    ".o_form_view.o_form_editable .o_field_widget[name='operating_unit_id']",
                run: function () {
                    // Assertion only; the field's presence is what we verify.
                },
            },
        ]
    );
});
