# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipTimesheet(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition: the Payslips menu is gated by the payslip access groups.
        # Granting the validator group to admin implies the user and viewer groups
        # (see ssi_hr_payroll/security/res_group_data.xml), so admin can open the
        # menu and the payslip form. Without it the tour would fail on the first
        # menu step.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        # Pre-Condition master data — prerequisites the payslip needs to be created,
        # not the focus of the tour (built in Python). Codes are distinct from the
        # base module's UI-test data to avoid collisions when the full suite runs.
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.debit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Timesheet Payroll Debit Account",
                "code": "TOURTSDB",
                "user_type_id": expense_type.id,
            }
        )
        cls.credit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Timesheet Payroll Credit Account",
                "code": "TOURTSCR",
                "user_type_id": expense_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Timesheet Payroll Journal",
                "code": "TOURTSJ",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR Timesheet Category",
                "code": "TOURTSCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR Timesheet Salary Rule",
                "code": "TOURTSRULE",
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
                "name": "TOUR Timesheet Salary Structure",
                "code": "TOURTSSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )
        cls.payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "TOUR TIMESHEET PAYSLIP TYPE",
                "code": "TOURTSTYPE",
                "journal_id": cls.journal.id,
            }
        )

        # Employee used to find the payslip row in the list (stable marker).
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR PAYSLIP TIMESHEET",
                "salary_structure_id": cls.structure.id,
            }
        )

        # Pre-Condition: a draft payslip the tour opens to view the Timesheet tab.
        # The timesheet_computation_ids field is computed from employee/period, so
        # no timesheet rows are needed — the tour only asserts the tab is shown.
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

    def test_tab_timesheet(self):
        """IK: docs/hr_payslip/01-create.md (E1 delta — Timesheet tab)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_timesheet_hr_payslip_tab_timesheet",
            login="admin",
        )
