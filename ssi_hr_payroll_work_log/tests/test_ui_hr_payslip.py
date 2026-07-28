# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipWorkLog(HttpSavepointCase):
    """Tour: assert the Work Log tab renders on the payslip form."""

    @classmethod
    def setUpClass(cls):
        """Grant admin access and build a computed payslip for the tour."""
        super().setUpClass()
        # Pre-Condition: the Payslips menu is gated by the payslip access groups.
        # Granting the validator group to admin implies the user and viewer
        # groups, so admin can open the menu and the payslip form. Without it the
        # tour would fail on the very first menu step.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        # Pre-Condition master data — prerequisites the payslip needs to be
        # computed, not the focus of the tour (built in Python).
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.debit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Payroll WL Debit Account",
                "code": "TOURWLDB",
                "user_type_id": expense_type.id,
            }
        )
        cls.credit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Payroll WL Credit Account",
                "code": "TOURWLCR",
                "user_type_id": expense_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Payroll WL Journal",
                "code": "TOURWL",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR WL Category",
                "code": "TOURWLCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR WL Salary Rule",
                "code": "TOURWLRULE",
                "category_id": cls.category.id,
                "debit_account_id": cls.debit_account.id,
                "credit_account_id": cls.credit_account.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        cls.structure = cls.env["hr.salary_structure"].create(
            {
                "name": "TOUR WL Salary Structure",
                "code": "TOURWLSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )
        cls.payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "TOUR WL PAYSLIP TYPE",
                "code": "TOURWLTYPE",
                "journal_id": cls.journal.id,
            }
        )

        # Payslip the tour opens to assert the Work Log tab. The employee name is
        # the stable marker the tour uses to find the row in the Payslips list.
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR PAYSLIP WORK LOG",
                "salary_structure_id": cls.structure.id,
            }
        )
        cls.payslip = cls.env["hr.payslip"].create(
            {
                "employee_id": cls.employee.id,
                "type_id": cls.payslip_type.id,
                "structure_id": cls.structure.id,
                "journal_id": cls.journal.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-31",
                "date": "2024-01-31",
            }
        )
        cls.payslip.action_compute_payslip()

    def test_tab_work_log(self):
        """IK: docs/hr_payslip/01-create.md (E1 delta — Work Log tab)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_work_log_hr_payslip_tab_work_log",
            login="admin",
        )
