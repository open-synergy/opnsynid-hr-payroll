# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatchWorkLog(HttpSavepointCase):
    """Tour the Work Log tab added to the ``hr.payslip_batch`` form."""

    @classmethod
    def setUpClass(cls):
        """Grant batch access and build the draft batch the tour opens."""
        super().setUpClass()
        # Pre-Condition: the Payslip Batches menu is gated by the batch access
        # groups. Granting the batch Validator group to admin implies the batch
        # User and Viewer groups, so admin can open the menu and the batch form.
        # Without it the tour would fail on the very first menu step.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_validator_group"
        ).sudo().write({"users": [(4, cls.user_admin.id)]})

        # Pre-Condition master data — prerequisites the batch needs, not the focus
        # of the tour (built in Python).
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Batch WL Journal",
                "code": "TOURBWL",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR Batch WL Category",
                "code": "TOURBWLCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR Batch WL Salary Rule",
                "code": "TOURBWLRULE",
                "category_id": cls.category.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        cls.structure = cls.env["hr.salary_structure"].create(
            {
                "name": "TOUR Batch WL Salary Structure",
                "code": "TOURBWLSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )
        # The batch is found in the list by the Type shown in the Type column, so
        # it uses a distinctly-named payslip type as the stable marker.
        cls.payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "TOUR BATCH WORK LOG",
                "code": "TOURBWLTYPE",
                "journal_id": cls.journal.id,
            }
        )
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR BATCH WORK LOG EMP",
                "salary_structure_id": cls.structure.id,
            }
        )

        # Draft batch the tour opens to assert the Work Log tab.
        cls.batch = cls.env["hr.payslip_batch"].create(
            {
                "type_id": cls.payslip_type.id,
                "journal_id": cls.journal.id,
                "date": "2024-01-31",
                "date_start": "2024-01-01",
                "date_end": "2024-01-31",
                "employee_ids": [(6, 0, [cls.employee.id])],
            }
        )

    def test_tab_work_log(self):
        """IK: docs/hr_payslip_batch/01-create.md (E1 delta — Work Log tab)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_work_log_hr_payslip_batch_tab_work_log",
            login="admin",
        )
