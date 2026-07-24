# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatchReportButtons(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Pre-Condition: opening a batch (leaving Draft) is gated by the batch
        # access groups. Granting the batch Validator group to admin implies the
        # batch User group so action_open succeeds in setUpClass. The report
        # buttons themselves are gated only by state, not by a group.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_validator_group"
        ).sudo().write({"users": [(4, cls.user_admin.id)]})

        # Pre-Condition master data — prerequisites the batch needs to generate
        # and compute payslips, not the focus of the tour (built in Python).
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.debit_account = cls.env["account.account"].create(
            {
                "name": "TOUR SUMMARY Debit Account",
                "code": "TOURSMDB",
                "user_type_id": expense_type.id,
            }
        )
        cls.credit_account = cls.env["account.account"].create(
            {
                "name": "TOUR SUMMARY Credit Account",
                "code": "TOURSMCR",
                "user_type_id": expense_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR SUMMARY Journal",
                "code": "TOURSM",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR SUMMARY Category",
                "code": "TOURSMCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR SUMMARY Salary Rule",
                "code": "TOURSMRULE",
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
                "name": "TOUR SUMMARY Salary Structure",
                "code": "TOURSMSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )

        # Each batch is found in the list by the Type shown in the Type column,
        # so every batch uses a distinctly-named payslip type.
        #
        # Non-draft batch: opened (In Progress) with payslips computed, so both
        # report buttons are visible & enabled.
        cls.batch_nondraft = cls._prepare_batch("TOUR SUMMARY NONDRAFT", "TOURSMTND")
        cls.batch_nondraft.with_context(bypass_policy_check=True).action_open()
        cls.batch_nondraft.action_compute_payslip()

        # Draft batch: left in Draft, so both report buttons stay hidden.
        cls.batch_draft = cls._prepare_batch("TOUR SUMMARY DRAFT", "TOURSMTD")

    @classmethod
    def _prepare_batch(cls, type_name, type_code):
        """Create a draft batch with one employee, tagged by a uniquely-named
        payslip type.

        The type name is the stable marker the tour uses to find the batch row
        in the Payslip Batches list (shown in the Type column).
        """
        payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": type_name,
                "code": type_code,
                "journal_id": cls.journal.id,
            }
        )
        employee = cls.env["hr.employee"].create(
            {
                "name": "%s EMP" % type_name,
                "salary_structure_id": cls.structure.id,
            }
        )
        batch = cls.env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "journal_id": cls.journal.id,
                "date": "2024-01-31",
                "date_start": "2024-01-01",
                "date_end": "2024-01-31",
                "employee_ids": [(6, 0, [employee.id])],
            }
        )
        return batch

    def test_report_buttons(self):
        """IK: docs/hr_payslip_batch/20-salary-summary-report.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_summary_report_hr_payslip_batch_report_buttons",
            login="admin",
        )
