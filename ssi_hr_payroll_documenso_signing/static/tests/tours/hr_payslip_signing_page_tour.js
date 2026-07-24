odoo.define("ssi_hr_payroll_documenso_signing.hr_payslip_signing_page_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/01-create.md (E2a delta — Modified Flow)
    // Re-trace the base create navigation up to the point of change (the
    // payslip form renders), then assert the delta: the Documenso Signing
    // page — visible tab label "Signature Requests" — is present in the
    // notebook. No external Documenso service is involved.
    tour.register(
        "ssi_hr_payroll_documenso_signing_hr_payslip_signing_page",
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
                // Gate on the TARGET action title: opening the app lands on
                // its first menu, so a generic ".o_list_view" would match the
                // stale landing view and let the next steps run on the wrong
                // screen.
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

            // ── Delta (point of change) — the Documenso Signing page appears
            // in the notebook as the "Signature Requests" tab.
            {
                content: "The Documenso Signing tab (Signature Requests) is present",
                trigger:
                    ".o_form_view .o_notebook .nav-link:contains(Signature Requests)",
                extra_trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; verify the tab is rendered and visible.
                },
            },
        ]
    );
});
