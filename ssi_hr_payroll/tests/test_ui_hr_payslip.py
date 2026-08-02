# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslip(HttpSavepointCase):
    """UI tour test suite for the ``hr.payslip`` state-transition flows."""

    @classmethod
    def setUpClass(cls):
        """Grant access group to admin and prepare payslips per tour state."""
        super().setUpClass()
        # Pre-Condition: the transaction state buttons (Confirm/Approve/Reject/
        # Cancel/Restart) and the Payslips menu are gated by the payslip access
        # groups. Granting the validator group to admin implies the user and
        # viewer groups (see security/res_group_data.xml), so admin can open the
        # menu, confirm, act as the approver, cancel and restart. Without it the
        # tours would fail on the very first menu step or find no action button.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        # Pre-Condition master data — prerequisites the payslip needs to be
        # computed and posted, not the focus of the tours (built in Python).
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.debit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Payroll Debit Account",
                "code": "TOURPRLDB",
                "user_type_id": expense_type.id,
            }
        )
        cls.credit_account = cls.env["account.account"].create(
            {
                "name": "TOUR Payroll Credit Account",
                "code": "TOURPRLCR",
                "user_type_id": expense_type.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Payroll Journal",
                "code": "TOURPRL",
                "type": "general",
            }
        )
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR Category",
                "code": "TOURPSLCAT",
            }
        )
        cls.rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR Salary Rule",
                "code": "TOURPSLRULE",
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
                "name": "TOUR Salary Structure",
                "code": "TOURPSLSTR",
                "rule_ids": [(6, 0, [cls.rule.id])],
            }
        )
        cls.payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "TOUR PAYSLIP TYPE",
                "code": "TOURPSLTYPE",
                "journal_id": cls.journal.id,
            }
        )
        # Pre-Condition for the cancel tour: a global-use cancellation reason so
        # it appears in the cancellation wizard for hr.payslip.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR CANCEL REASON",
                "code": "TOURCXL",
                "global_use": True,
            }
        )

        # Employee used by the create tour (selected through the UI).
        cls.env["hr.employee"].create(
            {
                "name": "TOUR PAYSLIP CREATE",
                "salary_structure_id": cls.structure.id,
            }
        )

        # Payslips prepared in the starting state each tour begins from.
        cls.payslip_edit = cls._prepare_payslip("TOUR PAYSLIP EDIT")
        cls.payslip_confirm = cls._prepare_payslip("TOUR PAYSLIP CONFIRM")
        cls.payslip_cancel = cls._prepare_payslip("TOUR PAYSLIP CANCEL")

        cls.payslip_approve = cls._prepare_payslip("TOUR PAYSLIP APPROVE")
        cls.payslip_approve.with_context(bypass_policy_check=True).action_confirm()

        cls.payslip_reject = cls._prepare_payslip("TOUR PAYSLIP REJECT")
        cls.payslip_reject.with_context(bypass_policy_check=True).action_confirm()

        cls.payslip_restart = cls._prepare_payslip("TOUR PAYSLIP RESTART")
        cls.payslip_restart.with_context(bypass_policy_check=True).action_cancel()

        # Pre-Condition for the restart-approval tour: ``restart_approval_ok``
        # (see policy_template_data.xml) only grants the button when the
        # confirmed record has NO ``approval_template_id`` yet — the
        # stalled-without-an-approver scenario the button exists to recover
        # from. The demo ``hr_payslip_approval_template`` matches every
        # payslip, so it is deactivated for the duration of this one
        # ``action_confirm`` call to keep ``approval_template_id`` empty,
        # then reactivated immediately so it is available again when the
        # tour itself clicks Restart Approval Process (and for every other
        # tour prepared below/after it).
        approval_template = cls.env.ref(
            "ssi_hr_payroll.hr_payslip_approval_template"
        ).sudo()
        cls.payslip_restart_approval = cls._prepare_payslip(
            "TOUR PAYSLIP RELOAD APPROVAL"
        )
        approval_template.write({"active": False})
        cls.payslip_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        approval_template.write({"active": True})

    @classmethod
    def _prepare_payslip(cls, employee_name):
        """Create a computed draft payslip for a uniquely-named employee.

        The employee name is the stable marker the tour uses to find the row
        in the Payslips list.
        """
        employee = cls.env["hr.employee"].create(
            {
                "name": employee_name,
                "salary_structure_id": cls.structure.id,
            }
        )
        payslip = cls.env["hr.payslip"].create(
            {
                "employee_id": employee.id,
                "type_id": cls.payslip_type.id,
                "structure_id": cls.structure.id,
                "journal_id": cls.journal.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-31",
                "date": "2024-01-31",
            }
        )
        payslip.action_compute_payslip()
        return payslip

    def test_create(self):
        """IK: docs/hr_payslip/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/hr_payslip/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_edit",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/hr_payslip/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/hr_payslip/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/hr_payslip/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/hr_payslip/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_cancel",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/hr_payslip/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """IK: docs/hr_payslip/14-restart-approval.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_payslip_restart_approval",
            login="admin",
        )
