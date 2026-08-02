# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatch(HttpSavepointCase):
    """Tour tests covering every ``hr.payslip_batch`` work instruction."""

    @classmethod
    def setUpClass(cls):
        """Prepare the access groups and records every batch tour needs.

        Adds ``admin`` to the batch and payslip validator groups so the
        state buttons are visible, then creates the payroll master data
        and one batch per tour starting state.
        """
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

        cls.batch_edit = cls._prepare_batch("TOUR BATCH EDIT", "TOURBTCTE")

        cls.batch_recompute = cls._prepare_batch("TOUR BATCH RECOMPUTE", "TOURBTCTRC")
        cls.batch_recompute.with_context(bypass_policy_check=True).action_open()

        cls.batch_export_input = cls._prepare_batch(
            "TOUR BATCH EXPORT INPUT", "TOURBTCTEI"
        )
        cls.batch_export_input.with_context(bypass_policy_check=True).action_open()

        cls.batch_import_input = cls._prepare_batch(
            "TOUR BATCH IMPORT INPUT", "TOURBTCTII"
        )
        cls.batch_import_input.with_context(bypass_policy_check=True).action_open()

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

        # Pre-Condition for the restart-approval tour: ``restart_approval_ok``
        # (see policy_template_data.xml) only grants the button when the
        # confirmed record has NO ``approval_template_id`` yet — the
        # stalled-without-an-approver scenario the button exists to recover
        # from. The demo ``hr_payslip_batch_approval_template`` matches every
        # batch, so it is deactivated for the duration of this one
        # ``action_confirm`` call to keep ``approval_template_id`` empty,
        # then reactivated immediately so it is available again when the
        # tour itself clicks Restart Approval Process.
        approval_template = cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_approval_template"
        ).sudo()
        cls.batch_restart_approval = cls._prepare_batch(
            "TOUR BATCH RESTART APPROVAL", "TOURBTCTRA"
        )
        cls.batch_restart_approval.with_context(bypass_policy_check=True).action_open()
        cls.batch_restart_approval.action_compute_payslip()
        approval_template.write({"active": False})
        cls.batch_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        approval_template.write({"active": True})

        # Pre-Condition for the print tour: a ``print_document_type`` linking
        # a report to ``hr.payslip_batch`` is required for the wizard to have
        # a report to offer — without it the wizard still opens but the
        # report list is empty. The tour itself never selects nor prints the
        # report (see test_print docstring), so the report action is a
        # placeholder that is never rendered.
        cls.print_report_action = cls.env["ir.actions.report"].create(
            {
                "name": "TOUR Payslip Batch Report",
                "model": "hr.payslip_batch",
                "report_type": "qweb-pdf",
                "report_name": "ssi_hr_payroll_batch.tour_payslip_batch_report",
            }
        )
        cls.env["print_document_type"].create(
            {
                "name": "TOUR Batch Print Type",
                "model_id": cls.env["ir.model"]._get_id("hr.payslip_batch"),
                "report_ids": [(6, 0, [cls.print_report_action.id])],
            }
        )

        cls.batch_print = cls._prepare_batch("TOUR BATCH PRINT", "TOURBTCTP")

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

    def test_edit(self):
        """Run the edit tour for ``hr.payslip_batch``.

        IK: docs/hr_payslip_batch/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_edit",
            login="admin",
        )

    def test_recompute(self):
        """Run the re-compute tour for ``hr.payslip_batch``.

        IK: docs/hr_payslip_batch/14-recompute.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_recompute",
            login="admin",
        )

    def test_export_input(self):
        """Run the export input tour for ``hr.payslip_batch``.

        Only asserts the Export Input button is visible and enabled on an
        In Progress batch; does not click it. Clicking triggers an
        ``ir.actions.act_url`` file download that a tour has no DOM signal
        to await, and could hang headless Chrome — a deliberate,
        documented limitation, not a disabled tour.

        IK: docs/hr_payslip_batch/15-export-input.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_export_input",
            login="admin",
        )

    def test_import_input(self):
        """Run the import input tour for ``hr.payslip_batch``.

        Only asserts the Import Input wizard opens, then closes it without
        uploading a file. There is no reliable DOM signal a tour can use to
        attach a file to a hidden ``<input type="file">`` across browsers;
        the wizard's ``action_import`` behavior is covered separately by a
        plain Python test instead — a deliberate, documented limitation,
        not a disabled tour.

        IK: docs/hr_payslip_batch/16-import-input.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_import_input",
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

    def test_restart_approval_process(self):
        """IK: docs/hr_payslip_batch/17-restart-approval.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_restart_approval",
            login="admin",
        )

    def test_print(self):
        """Assert the Print wizard opens then close it, without printing.

        IK: docs/hr_payslip_batch/18-print.md

        Boundary: the tour only proves the ``Select Report To Print`` wizard
        opens after clicking Print, then closes it via Cancel. It never
        selects a report nor clicks the wizard's own Print button, because
        the resulting report action is an ``ir.actions.act_url`` download
        with no DOM "finished" signal — clicking through it could hang
        headless Chrome. See patterns.md §Q.
        """
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_hr_payslip_batch_print",
            login="admin",
        )
