# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatch(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition: the batch state buttons are gated by the batch access
        # groups (open_ok/confirm_ok use the batch User group; approve_ok/reject_ok
        # require the user to be an approver) and by the payslip Validator group
        # (cancel_ok/restart_ok). Granting the batch Validator group implies the
        # batch User group and makes admin an approver on the Standard approval
        # template; granting the payslip Validator group enables Cancel/Restart.
        # Without these the tours would fail on the menu step or find no button.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_validator_group"
        ).sudo().write({"users": [(4, cls.user_admin.id)]})
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

        # Pre-Condition master data — prerequisites the batch needs to generate,
        # compute and post payslips, not the focus of the tours (built in Python).
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.debit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Batch Debit Account",
                "code": "TOURBTCDB",
                "user_type_id": expense_type.id,
            }
        )
        cls.credit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Batch Credit Account",
                "code": "TOURBTCCR",
                "user_type_id": expense_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Batch Journal",
                "code": "TOURBTC",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR Batch Category",
                "code": "TOURBTCCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR Batch Salary Rule",
                "code": "TOURBTCRULE",
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
                "name": "TOUR Batch Salary Structure",
                "code": "TOURBTCSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )

        # Pre-Condition for the cancel tour: a global-use cancellation reason so it
        # appears in the cancellation wizard for hr.payslip_batch.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR CANCEL REASON",
                "code": "TOURBTCCXL",
                "global_use": True,
            }
        )

        # Each tour finds its batch in the list by the Type shown in the Type
        # column, so every batch uses a distinctly-named payslip type. The create
        # tour selects "TOUR BATCH CREATE" through the UI; an employee with a
        # salary structure is prepared so the Reload button has something to load.
        cls._create_type("TOUR BATCH CREATE", "TOURBTCTC")
        cls.env["hr.employee"].create(
            {
                "name": "TOUR BATCH CREATE EMP",
                "salary_structure_id": cls.structure.id,
            }
        )

        # Batches prepared in the starting state each tour begins from.
        cls.batch_start = cls._prepare_batch("TOUR BATCH START", "TOURBTCTS")

        cls.batch_confirm = cls._prepare_batch("TOUR BATCH CONFIRM", "TOURBTCTCF")
        cls.batch_confirm.with_context(bypass_policy_check=True).action_open()
        cls.batch_confirm.action_compute_payslip()

        cls.batch_approve = cls._prepare_batch("TOUR BATCH APPROVE", "TOURBTCTA")
        cls.batch_approve.with_context(bypass_policy_check=True).action_open()
        cls.batch_approve.action_compute_payslip()
        cls.batch_approve.with_context(bypass_policy_check=True).action_confirm()

        cls.batch_reject = cls._prepare_batch("TOUR BATCH REJECT", "TOURBTCTR")
        cls.batch_reject.with_context(bypass_policy_check=True).action_open()
        cls.batch_reject.action_compute_payslip()
        cls.batch_reject.with_context(bypass_policy_check=True).action_confirm()

        cls.batch_cancel = cls._prepare_batch("TOUR BATCH CANCEL", "TOURBTCTCX")

        cls.batch_restart = cls._prepare_batch("TOUR BATCH RESTART", "TOURBTCTRS")
        cls.batch_restart.with_context(bypass_policy_check=True).action_cancel()

    @classmethod
    def _create_type(cls, name, code):
        """Create a payslip type wired to the shared batch journal."""
        return cls.env["hr.payslip_type"].create(
            {
                "name": name,
                "code": code,
                "journal_id": cls.journal.id,
            }
        )

    @classmethod
    def _prepare_batch(cls, type_name, type_code):
        """Create a draft batch with one employee, tagged by a uniquely-named
        payslip type.

        The type name is the stable marker the tour uses to find the batch row
        in the Payslip Batches list (shown in the Type column).
        """
        payslip_type = cls._create_type(type_name, type_code)
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

    def test_create(self):
        """IK: docs/hr_payslip_batch/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_create",
            login="admin",
        )

    def test_start(self):
        """IK: docs/hr_payslip_batch/07-start.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_start",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/hr_payslip_batch/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/hr_payslip_batch/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/hr_payslip_batch/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/hr_payslip_batch/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_cancel",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/hr_payslip_batch/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_restart",
            login="admin",
        )
