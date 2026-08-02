odoo.define("ssi_hr_payroll.hr_payslip_restart_approval_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_payslip/14-restart-approval.md
    tour.register(
        "ssi_hr_payroll_hr_payslip_restart_approval",
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

            // ── Flow 2 — Open the payslip whose approval process is stalled.
            // The Pre-Condition record (Waiting for Approval, without an
            // approval template assigned) is prepared in setUpClass for
            // employee "TOUR PAYSLIP RELOAD APPROVAL".
            {
                content: "Open the payslip",
                trigger:
                    ".o_data_row:contains(TOUR PAYSLIP RELOAD APPROVAL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Payslip form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Restart Approval Process button.
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status remains Waiting for Approval, and the
            // Approvals tab displays the approval list newly formed from the
            // approval template. Row count/content is out of tour scope
            // (unit test territory); the gate below only proves the reload
            // happened — the Pre-Condition record has no approval template
            // and no approval line at all, so a row cannot appear here
            // unless the restart actually ran (patterns.md §P).
            {
                content: "Open the Approvals tab",
                trigger: ".o_notebook .nav-link:contains(Approvals)",
                extra_trigger: "body:not(:has(.modal))",
            },
            {
                content: "The approval process has been rebuilt",
                trigger: ".o_field_widget[name='approval_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Status is still Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
