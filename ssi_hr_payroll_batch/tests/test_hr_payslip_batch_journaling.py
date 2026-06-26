# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, tagged

from odoo.addons.ssi_hr_payroll_batch.tests.test_hr_payslip_batch import (
    TestHrPayslipBatch,
)


@tagged("post_install", "-at_install")
class TestHrPayslipBatchJournaling(TestHrPayslipBatch):
    """Tests for batch-level journaling (plan §5, tests 3-15 + 17-18)."""

    # ------------------------------------------------------------------ #
    #  fixture helpers                                                     #
    # ------------------------------------------------------------------ #

    def _create_batch_journaling_fixtures(self, prefix, n_employees=2):
        """Return a dict of fixtures for journaling tests."""
        env = self.env
        acc_type = env.ref("account.data_account_type_expenses")

        debit_acc = env["account.account"].create(
            {
                "name": "%s Debit" % prefix,
                "code": "%sDB" % prefix,
                "user_type_id": acc_type.id,
            }
        )
        credit_acc = env["account.account"].create(
            {
                "name": "%s Credit" % prefix,
                "code": "%sCR" % prefix,
                "user_type_id": acc_type.id,
            }
        )
        default_acc = env["account.account"].create(
            {
                "name": "%s Default" % prefix,
                "code": "%sDFT" % prefix,
                "user_type_id": acc_type.id,
            }
        )
        journal = env["account.journal"].create(
            {
                "name": "%s Journal" % prefix,
                "code": prefix[:4],
                "type": "general",
                "default_account_id": default_acc.id,
            }
        )
        rule_cat = env["hr.salary_rule_category"].create(
            {"name": "%s Cat" % prefix, "code": "%sCAT" % prefix}
        )
        rule = env["hr.salary_rule"].create(
            {
                "name": "%s Rule" % prefix,
                "code": "%sRULE" % prefix,
                "category_id": rule_cat.id,
                "debit_account_id": debit_acc.id,
                "credit_account_id": credit_acc.id,
                "condition_python": "result = True",
                "amount_python": "result = 1000.0",
                "sequence": 10,
            }
        )
        structure = env["hr.salary_structure"].create(
            {
                "name": "%s Structure" % prefix,
                "code": "%sSTR" % prefix,
                "rule_ids": [(4, rule.id)],
            }
        )
        payslip_type = env["hr.payslip_type"].create(
            {
                "name": "%s Type" % prefix,
                "code": "%sTYPE" % prefix,
                "accounting_method": "batch",
                "journal_id": journal.id,
            }
        )
        struct_field = (
            "manual_salary_structure_id"
            if "manual_salary_structure_id" in env["hr.employee"]._fields
            else "salary_structure_id"
        )
        employees = []
        for i in range(n_employees):
            emp = env["hr.employee"].create(
                {
                    "name": "%s Employee %d" % (prefix, i + 1),
                    struct_field: structure.id,
                }
            )
            employees.append(emp)

        batch = env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "accounting_method": "batch",
                "journal_id": journal.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "date": "2026-01-31",
                "employee_ids": [(6, 0, [e.id for e in employees])],
            }
        )
        return {
            "batch": batch,
            "journal": journal,
            "debit_acc": debit_acc,
            "credit_acc": credit_acc,
            "rule": rule,
            "structure": structure,
            "payslip_type": payslip_type,
            "employees": employees,
        }

    def _run_batch_to_done(self, batch):
        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).action_open()
        batch.invalidate_cache()
        batch.with_user(admin).action_compute_payslip()
        batch.invalidate_cache()
        batch.with_user(admin).with_context(bypass_policy_check=True).action_confirm()
        batch.invalidate_cache()
        batch.with_user(admin).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        batch.invalidate_cache()

    # ------------------------------------------------------------------ #
    #  Tests 1-2: default / payslip-method regression                     #
    # ------------------------------------------------------------------ #

    def test_01_default_accounting_method_is_payslip(self):
        """Test 1: A new batch defaults to accounting_method='payslip'."""
        journal = self.env["account.journal"].create(
            {"name": "T1 Journal", "code": "T1JRN", "type": "general"}
        )
        ptype = self.env["hr.payslip_type"].create(
            {"name": "T1 Type", "code": "T1TYPE", "journal_id": journal.id}
        )
        batch = self.env["hr.payslip_batch"].create(
            {
                "type_id": ptype.id,
                "date_start": "2026-02-01",
                "date_end": "2026-02-28",
                "date": "2026-02-28",
            }
        )
        self.assertEqual(batch.accounting_method, "payslip")

    # ------------------------------------------------------------------ #
    #  Test 3: payslips are done without a move (batch method)            #
    # ------------------------------------------------------------------ #

    def test_03_payslips_done_without_move_in_batch_method(self):
        """Test 3: Payslips are done but have no move_id when method=batch."""
        f = self._create_batch_journaling_fixtures("T3", n_employees=1)
        batch = f["batch"]
        self._run_batch_to_done(batch)

        self.assertEqual(batch.state, "done")
        for payslip in batch.payslip_ids:
            self.assertEqual(payslip.state, "done")
            self.assertFalse(
                payslip.move_id,
                "Payslip should NOT have a move_id when batch method is used",
            )

    # ------------------------------------------------------------------ #
    #  Test 4: single batch move, posted & balanced                       #
    # ------------------------------------------------------------------ #

    def test_04_batch_move_posted_and_balanced(self):
        """Test 4: Batch has a single posted balanced move."""
        f = self._create_batch_journaling_fixtures("T4", n_employees=1)
        batch = f["batch"]
        self._run_batch_to_done(batch)

        self.assertTrue(batch.move_id, "Batch should have a move_id")
        self.assertEqual(batch.move_id.state, "posted")
        total_debit = sum(batch.move_id.line_ids.mapped("debit"))
        total_credit = sum(batch.move_id.line_ids.mapped("credit"))
        self.assertAlmostEqual(total_debit, total_credit, places=2)

    # ------------------------------------------------------------------ #
    #  Test 5: merge by rule across employees                             #
    # ------------------------------------------------------------------ #

    def test_05_rule_with_no_contributor_merged_across_employees(self):
        """Test 5: RULE_BASIC (no contributor) → one debit + one credit AML."""
        f = self._create_batch_journaling_fixtures("T5", n_employees=2)
        batch = f["batch"]
        self._run_batch_to_done(batch)

        debit_acc = f["debit_acc"]
        credit_acc = f["credit_acc"]
        move_lines = batch.move_id.line_ids

        debit_lines_on_rule = move_lines.filtered(
            lambda l: l.account_id == debit_acc and l.debit > 0
        )
        credit_lines_on_rule = move_lines.filtered(
            lambda l: l.account_id == credit_acc and l.credit > 0
        )
        self.assertEqual(
            len(debit_lines_on_rule),
            1,
            "Should have exactly ONE debit AML for the basic rule",
        )
        self.assertEqual(
            len(credit_lines_on_rule),
            1,
            "Should have exactly ONE credit AML for the basic rule",
        )
        # Amount must equal sum of both payslip amounts (2 * 1000)
        self.assertAlmostEqual(debit_lines_on_rule[0].debit, 2000.0, places=2)
        self.assertAlmostEqual(credit_lines_on_rule[0].credit, 2000.0, places=2)

    # ------------------------------------------------------------------ #
    #  Test 8: cancel removes the batch move                              #
    # ------------------------------------------------------------------ #

    def test_08_cancel_removes_batch_move(self):
        """Test 8: Cancelling the batch removes its move_id."""
        f = self._create_batch_journaling_fixtures("T8", n_employees=1)
        batch = f["batch"]
        self._run_batch_to_done(batch)

        move_id = batch.move_id.id
        self.assertTrue(move_id)

        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).with_context(bypass_policy_check=True).action_cancel()
        batch.invalidate_cache()

        self.assertFalse(batch.move_id, "Batch move_id should be cleared after cancel")
        move_exists = self.env["account.move"].search([("id", "=", move_id)])
        self.assertFalse(move_exists, "account.move should be deleted after cancel")

    # ------------------------------------------------------------------ #
    #  Test 9: cancel → restart → done re-journals cleanly               #
    # ------------------------------------------------------------------ #

    def test_09_cancel_restart_done_rejournals_cleanly(self):
        """Test 9: Cancel → Restart → Done produces a single fresh balanced move."""
        f = self._create_batch_journaling_fixtures("T9", n_employees=1)
        batch = f["batch"]
        self._run_batch_to_done(batch)

        # Cancel
        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).with_context(bypass_policy_check=True).action_cancel()
        batch.invalidate_cache()
        self.assertFalse(batch.move_id)

        # Restart → draft
        batch.with_user(admin).with_context(bypass_policy_check=True).action_restart()
        batch.invalidate_cache()
        self.assertEqual(batch.state, "draft")

        # Re-run to done
        self._run_batch_to_done(batch)

        self.assertTrue(
            batch.move_id, "Batch should have a new move after re-journaling"
        )
        self.assertEqual(batch.move_id.state, "posted")
        total_debit = sum(batch.move_id.line_ids.mapped("debit"))
        total_credit = sum(batch.move_id.line_ids.mapped("credit"))
        self.assertAlmostEqual(total_debit, total_credit, places=2)

        # No duplicate entries
        rule = f["rule"]
        entry_count = len(batch.account_entry_ids.filtered(lambda e: e.rule_id == rule))
        self.assertEqual(
            entry_count, 1, "Should have exactly one entry per rule, not duplicates"
        )

    # ------------------------------------------------------------------ #
    #  Test 15: lock — direct payslip action raises                       #
    # ------------------------------------------------------------------ #

    def test_15_locked_payslip_action_raises(self):
        """Test 15: Calling payslip.action_confirm() directly while batch_id is set raises."""
        f = self._create_batch_journaling_fixtures("T15", n_employees=1)
        batch = f["batch"]

        # Open the batch to generate payslips
        admin = self.env.ref("base.user_admin")
        batch.with_user(admin).action_open()
        batch.invalidate_cache()

        payslip = batch.payslip_ids[0]
        self.assertTrue(payslip.batch_id)

        with self.assertRaises(UserError):
            payslip.action_confirm()

    # ------------------------------------------------------------------ #
    #  Tests 17-18: onchange / constraint                                 #
    # ------------------------------------------------------------------ #

    def test_17_onchange_type_id_copies_accounting_method(self):
        """Test 17: Setting type_id with accounting_method='batch' copies it to the batch."""
        journal = self.env["account.journal"].create(
            {"name": "T17 Journal", "code": "T17J", "type": "general"}
        )
        ptype_batch = self.env["hr.payslip_type"].create(
            {
                "name": "T17 Batch Type",
                "code": "T17BT",
                "accounting_method": "batch",
                "journal_id": journal.id,
            }
        )
        ptype_payslip = self.env["hr.payslip_type"].create(
            {
                "name": "T17 Payslip Type",
                "code": "T17PT",
                "accounting_method": "payslip",
                "journal_id": journal.id,
            }
        )
        form = Form(self.env["hr.payslip_batch"])
        form.type_id = ptype_batch
        self.assertEqual(form.accounting_method, "batch")
        self.assertEqual(form.journal_id.id, journal.id)

        form.type_id = ptype_payslip
        self.assertEqual(form.accounting_method, "payslip")

    def test_18_journal_id_constraint_batch_method_no_journal_raises(self):
        """Test 18: Confirming a batch with method=batch and no journal_id raises."""
        self.env.ref("account.data_account_type_expenses")
        journal = self.env["account.journal"].create(
            {"name": "T18 Journal", "code": "T18J", "type": "general"}
        )
        ptype = self.env["hr.payslip_type"].create(
            {
                "name": "T18 Type",
                "code": "T18TYPE",
                "accounting_method": "batch",
                "journal_id": journal.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["hr.payslip_batch"].create(
                {
                    "type_id": ptype.id,
                    "accounting_method": "batch",
                    "journal_id": False,
                    "date_start": "2026-03-01",
                    "date_end": "2026-03-31",
                    "date": "2026-03-31",
                }
            )

    def test_18b_payslip_method_without_journal_allowed(self):
        """Test 18b: method=payslip without journal_id is allowed."""
        journal = self.env["account.journal"].create(
            {"name": "T18b Journal", "code": "T18BJ", "type": "general"}
        )
        ptype = self.env["hr.payslip_type"].create(
            {
                "name": "T18b Type",
                "code": "T18BTYPE",
                "accounting_method": "payslip",
                "journal_id": journal.id,
            }
        )
        # Should NOT raise
        batch = self.env["hr.payslip_batch"].create(
            {
                "type_id": ptype.id,
                "accounting_method": "payslip",
                "journal_id": False,
                "date_start": "2026-04-01",
                "date_end": "2026-04-30",
                "date": "2026-04-30",
            }
        )
        self.assertEqual(batch.accounting_method, "payslip")
