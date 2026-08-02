# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrSalaryContribution(HttpSavepointCase):
    """UI tour test suite for the ``hr.salary_contribution`` menu."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group to admin and prepare print data."""
        super().setUpClass()
        # Pre-Condition: the Salary Contributions master data menu is gated by the
        # Salary Contribution configurator group. Without it the tour would fail on
        # its very first step because the menu is not rendered at all.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_configurator = cls.env.ref(
            "ssi_hr_payroll.hr_salary_contribution_configurator_group"
        )
        cls.group_configurator.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        # Pre-Condition for Generate Code (docs/hr_salary_contribution/01-create.md
        # and 02-edit.md): an active ``sequence.template`` for this model is
        # required, or clicking the button raises a UserError instead of
        # assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Salary Contribution Code Sequence",
                "code": "ssi_hr_payroll.tour.hr_salary_contribution",
                "prefix": "TOURSEQSC",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Salary Contribution Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("hr.salary_contribution"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("hr.salary_contribution", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("hr.salary_contribution", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        # Pre-Condition for the print tour: a ``print_document_type``
        # linking a report to ``hr.salary_contribution`` is required for
        # the wizard to have a report to offer — without it the wizard
        # still opens but the report list is empty. The tour itself never
        # selects nor prints the report (see test_print docstring), so the
        # report action is a placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Salary Contribution Report",
                "model": "hr.salary_contribution",
                "report_type": "qweb-pdf",
                "report_name": "ssi_hr_payroll.tour_salary_contribution_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Print Type",
                "model_id": cls.env["ir.model"]._get_id("hr.salary_contribution"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )
        cls.salary_contribution_print = cls.env["hr.salary_contribution"].create(
            {
                "name": "TOUR PRINT SALARY CONTRIBUTION",
                "code": "TOURPRNSC",
            }
        )

    def test_create(self):
        """IK: docs/hr_salary_contribution/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_salary_contribution_create",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/hr_salary_contribution/06-print.md

        Boundary: the tour only proves the ``Select Report To Print``
        wizard opens after clicking Print, then closes it via Cancel. It
        never selects a report nor clicks the wizard's own Print button,
        because the resulting report action is an ``ir.actions.act_url``
        download with no DOM "finished" signal — clicking through it
        could hang headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_salary_contribution_print",
            login="admin",
        )
