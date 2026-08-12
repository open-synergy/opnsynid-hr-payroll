# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchJournaling(YamlTransactionCase):
    """Tests for batch-level journaling (plan §5, tests 3-15 + 17-18)."""

    def test_hr_payslip_batch_journaling(self):
        """Runs the YAML default, state, lock, onchange and constraint
        cases for batch-level journaling."""
        self.run_yaml_scenario("test_data_hr_payslip_batch_journaling.yaml")

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
        """Drive ``batch`` from draft up to its ``done`` state as admin.

        Runs open, compute, confirm and approve with the approval policy
        bypassed, invalidating the cache between steps so the computed
        fields are re-read from database.

        :param batch: the ``hr.payslip_batch`` record to advance
        """
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
    #  Test 4: single batch move, posted & balanced                       #
    # ------------------------------------------------------------------ #

    def test_04_batch_move_posted_and_balanced(self):
        """Test 4: Batch has a single posted balanced move.

        Pure Python -- trigger P2 (L-04: ``equals`` has no float
        tolerance, so the ``sum()``-aggregated debit/credit totals
        cannot be asserted equal from YAML).
        """
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
        """Test 5: RULE_BASIC (no contributor) -> one debit + one credit
        AML.

        Pure Python -- trigger P3 (L-06: o2m comparisons are set-based
        and unordered; selecting the move lines that belong to a
        specific account requires filtering in Python).
        """
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
    #  Test 9: cancel → restart → done re-journals cleanly               #
    # ------------------------------------------------------------------ #

    def test_09_cancel_restart_done_rejournals_cleanly(self):
        """Test 9: Cancel -> Restart -> Done produces a single fresh
        balanced move.

        Pure Python -- trigger P2 (L-04: the debit/credit totals need
        ``sum()`` and a tolerant comparison, which YAML cannot
        express).
        """
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
    #  Task 4C: regression — paired one-sided rules without usage          #
    # ------------------------------------------------------------------ #

    def _create_one_sided_batch_fixtures(self):
        """Fixtures for paired one-sided rules (debit-only + credit-only) with no usage."""
        env = self.env
        acc_type = env.ref("account.data_account_type_expenses")

        debit_acc = env["account.account"].create(
            {"name": "OS Debit", "code": "OSDB01", "user_type_id": acc_type.id}
        )
        credit_acc = env["account.account"].create(
            {"name": "OS Credit", "code": "OSCR01", "user_type_id": acc_type.id}
        )
        default_acc = env["account.account"].create(
            {"name": "OS Default", "code": "OSDFT01", "user_type_id": acc_type.id}
        )
        journal = env["account.journal"].create(
            {
                "name": "OS Journal",
                "code": "OSJRN",
                "type": "general",
                "default_account_id": default_acc.id,
            }
        )
        rule_cat = env["hr.salary_rule_category"].create(
            {"name": "OS Cat", "code": "OSCAT"}
        )
        rule_debit = env["hr.salary_rule"].create(
            {
                "name": "OS Debit-Only Rule",
                "code": "OSDBRULE",
                "category_id": rule_cat.id,
                "debit_account_id": debit_acc.id,
                "condition_python": "result = True",
                "amount_python": "result = 500.0",
                "sequence": 10,
            }
        )
        rule_credit = env["hr.salary_rule"].create(
            {
                "name": "OS Credit-Only Rule",
                "code": "OSCRRULE",
                "category_id": rule_cat.id,
                "credit_account_id": credit_acc.id,
                "condition_python": "result = True",
                "amount_python": "result = 500.0",
                "sequence": 20,
            }
        )
        structure = env["hr.salary_structure"].create(
            {
                "name": "OS Structure",
                "code": "OSSTR",
                "rule_ids": [(4, rule_debit.id), (4, rule_credit.id)],
            }
        )
        payslip_type = env["hr.payslip_type"].create(
            {
                "name": "OS Type",
                "code": "OSTYPE",
                "accounting_method": "batch",
                "journal_id": journal.id,
            }
        )
        struct_field = (
            "manual_salary_structure_id"
            if "manual_salary_structure_id" in env["hr.employee"]._fields
            else "salary_structure_id"
        )
        employee = env["hr.employee"].create(
            {"name": "OS Employee", struct_field: structure.id}
        )
        batch = env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "accounting_method": "batch",
                "journal_id": journal.id,
                "date_start": "2026-05-01",
                "date_end": "2026-05-31",
                "date": "2026-05-31",
                "employee_ids": [(6, 0, [employee.id])],
            }
        )
        return {
            "batch": batch,
            "journal": journal,
            "debit_acc": debit_acc,
            "credit_acc": credit_acc,
            "default_acc": default_acc,
            "rule_debit": rule_debit,
            "rule_credit": rule_credit,
        }

    def test_20_paired_one_sided_rules_no_aml_with_false_account(self):
        """Regression Task 4C: paired one-sided rules -> no AML with
        account_id=False.

        Proves that ``_create_standard_ml()`` override correctly
        skips the missing side instead of creating an AML with
        account_id=False (which would fail ``action_post``).

        Pure Python -- trigger P3 (L-06: asserting the absence of a
        move line matching a criterion requires filtering the o2m in
        Python).
        """
        f = self._create_one_sided_batch_fixtures()
        batch = f["batch"]
        self._run_batch_to_done(batch)

        self.assertEqual(batch.state, "done")
        self.assertTrue(batch.move_id)
        self.assertEqual(batch.move_id.state, "posted")

        false_account_lines = batch.move_id.line_ids.filtered(
            lambda l: not l.account_id
        )
        self.assertFalse(
            false_account_lines,
            "Batch move must not contain any AML with account_id=False",
        )

    def test_21_paired_one_sided_rules_correct_aml_sides(self):
        """Regression Task 4C: debit-only -> 1 debit AML; credit-only ->
        1 credit AML.

        Pure Python -- trigger P3 (L-06: selecting and counting move
        lines by account requires filtering the o2m in Python, which
        YAML cannot express).
        """
        f = self._create_one_sided_batch_fixtures()
        batch = f["batch"]
        self._run_batch_to_done(batch)

        move_lines = batch.move_id.line_ids
        debit_lines = move_lines.filtered(
            lambda l: l.account_id == f["debit_acc"] and l.debit > 0
        )
        credit_lines = move_lines.filtered(
            lambda l: l.account_id == f["credit_acc"] and l.credit > 0
        )
        self.assertEqual(
            len(debit_lines),
            1,
            "Must have exactly one debit AML on the debit account",
        )
        self.assertEqual(
            len(credit_lines),
            1,
            "Must have exactly one credit AML on the credit account",
        )
        self.assertAlmostEqual(debit_lines[0].debit, 500.0, places=2)
        self.assertAlmostEqual(credit_lines[0].credit, 500.0, places=2)

    def test_22_paired_one_sided_rules_move_balanced(self):
        """Regression Task 4C: paired one-sided rules produce a balanced
        batch move.

        Pure Python -- trigger P2 (L-04: the debit/credit totals need
        ``sum()`` and a tolerant comparison, which YAML cannot
        express).
        """
        f = self._create_one_sided_batch_fixtures()
        batch = f["batch"]
        self._run_batch_to_done(batch)

        total_debit = sum(batch.move_id.line_ids.mapped("debit"))
        total_credit = sum(batch.move_id.line_ids.mapped("credit"))
        self.assertAlmostEqual(
            total_debit,
            total_credit,
            places=2,
            msg="Batch move must be balanced for paired one-sided rules",
        )

    # ------------------------------------------------------------------ #
    #  Gate semantics regression (fixed account = per-side gate)           #
    # ------------------------------------------------------------------ #

    def _create_gate_batch_fixtures(self):
        """Fixtures with batch usage + two rules:

        - rule_gate: has product + both fixed gate accounts; the batch usage
          resolves to DISTINCT usage accounts, so usage OVERRIDES the gate accounts.
        - rule_nogate: has product (usage resolves to its own accounts) but NO fixed
          accounts → under gate semantics it must NOT journal any side.
        """
        env = self.env
        acc_type = env.ref("account.data_account_type_expenses")

        def _acc(name, code):
            """Create an expense-type account for the gate fixtures.

            :param name: account name
            :param code: account code
            :return: the created ``account.account`` record
            """
            return env["account.account"].create(
                {"name": name, "code": code, "user_type_id": acc_type.id}
            )

        gate_debit = _acc("GT Gate Debit", "GTGDB")
        gate_credit = _acc("GT Gate Credit", "GTGCR")
        usage_debit = _acc("GT Usage Debit", "GTUDB")
        usage_credit = _acc("GT Usage Credit", "GTUCR")
        nogate_usage_debit = _acc("GT NoGate Usage Debit", "GTNDB")
        nogate_usage_credit = _acc("GT NoGate Usage Credit", "GTNCR")
        default_acc = _acc("GT Default", "GTDFT")

        journal = env["account.journal"].create(
            {
                "name": "GT Journal",
                "code": "GTJRN",
                "type": "general",
                "default_account_id": default_acc.id,
            }
        )
        debit_usage = env["product.usage_type"].create(
            {"name": "GT Debit Usage", "code": "GTUSGDB", "account_id": usage_debit.id}
        )
        credit_usage = env["product.usage_type"].create(
            {
                "name": "GT Credit Usage",
                "code": "GTUSGCR",
                "account_id": usage_credit.id,
            }
        )
        product_gate = env["product.product"].create({"name": "GT Product Gate"})
        product_nogate = env["product.product"].create({"name": "GT Product NoGate"})
        # product_gate resolves to the shared usage accounts.
        env["product.account"].create(
            {
                "product_id": product_gate.id,
                "usage_id": debit_usage.id,
                "account_id": usage_debit.id,
            }
        )
        env["product.account"].create(
            {
                "product_id": product_gate.id,
                "usage_id": credit_usage.id,
                "account_id": usage_credit.id,
            }
        )
        # product_nogate resolves to its OWN accounts (used to prove they never appear).
        env["product.account"].create(
            {
                "product_id": product_nogate.id,
                "usage_id": debit_usage.id,
                "account_id": nogate_usage_debit.id,
            }
        )
        env["product.account"].create(
            {
                "product_id": product_nogate.id,
                "usage_id": credit_usage.id,
                "account_id": nogate_usage_credit.id,
            }
        )
        rule_cat = env["hr.salary_rule_category"].create(
            {"name": "GT Cat", "code": "GTCAT"}
        )
        rule_gate = env["hr.salary_rule"].create(
            {
                "name": "GT Gate Rule",
                "code": "GTGATERULE",
                "category_id": rule_cat.id,
                "product_id": product_gate.id,
                "debit_account_id": gate_debit.id,
                "credit_account_id": gate_credit.id,
                "condition_python": "result = True",
                "amount_python": "result = 1000.0",
                "sequence": 10,
            }
        )
        rule_nogate = env["hr.salary_rule"].create(
            {
                "name": "GT NoGate Rule",
                "code": "GTNOGATERULE",
                "category_id": rule_cat.id,
                "product_id": product_nogate.id,
                "condition_python": "result = True",
                "amount_python": "result = 700.0",
                "sequence": 20,
            }
        )
        structure = env["hr.salary_structure"].create(
            {
                "name": "GT Structure",
                "code": "GTSTR",
                "rule_ids": [(4, rule_gate.id), (4, rule_nogate.id)],
            }
        )
        payslip_type = env["hr.payslip_type"].create(
            {
                "name": "GT Type",
                "code": "GTTYPE",
                "accounting_method": "batch",
                "journal_id": journal.id,
                "debit_usage_id": debit_usage.id,
                "credit_usage_id": credit_usage.id,
            }
        )
        struct_field = (
            "manual_salary_structure_id"
            if "manual_salary_structure_id" in env["hr.employee"]._fields
            else "salary_structure_id"
        )
        employee = env["hr.employee"].create(
            {"name": "GT Employee", struct_field: structure.id}
        )
        batch = env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "accounting_method": "batch",
                "journal_id": journal.id,
                "debit_usage_id": debit_usage.id,
                "credit_usage_id": credit_usage.id,
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
                "date": "2026-06-30",
                "employee_ids": [(6, 0, [employee.id])],
            }
        )
        return {
            "batch": batch,
            "gate_debit": gate_debit,
            "gate_credit": gate_credit,
            "usage_debit": usage_debit,
            "usage_credit": usage_credit,
            "nogate_usage_debit": nogate_usage_debit,
            "nogate_usage_credit": nogate_usage_credit,
        }

    def test_23_usage_overrides_gate_account_in_batch(self):
        """Gate present + batch usage resolves -> entry uses the USAGE
        account, not gate.

        Pure Python -- trigger P3 (L-06: asserting which specific move
        lines exist -- and which do not -- by account requires
        filtering the o2m in Python).
        """
        f = self._create_gate_batch_fixtures()
        batch = f["batch"]
        self._run_batch_to_done(batch)

        self.assertEqual(batch.move_id.state, "posted")
        move_lines = batch.move_id.line_ids

        self.assertTrue(
            move_lines.filtered(
                lambda l: l.account_id == f["usage_debit"] and l.debit > 0
            ),
            "Debit AML must land on the usage account, overriding the gate account",
        )
        self.assertTrue(
            move_lines.filtered(
                lambda l: l.account_id == f["usage_credit"] and l.credit > 0
            ),
            "Credit AML must land on the usage account, overriding the gate account",
        )
        self.assertFalse(
            move_lines.filtered(
                lambda l: l.account_id in (f["gate_debit"] + f["gate_credit"])
            ),
            "Gate accounts must NOT appear when usage resolves",
        )

    def test_24_no_gate_rule_does_not_journal_in_batch(self):
        """Gate empty: a rule without fixed accounts must NOT journal any
        side, even though its product usage resolves an account.

        Pure Python -- trigger P3 (L-06: asserting the absence of move
        lines on specific accounts requires filtering the o2m in
        Python).
        """
        f = self._create_gate_batch_fixtures()
        batch = f["batch"]
        self._run_batch_to_done(batch)

        move_lines = batch.move_id.line_ids
        self.assertFalse(
            move_lines.filtered(lambda l: not l.account_id),
            "Batch move must not contain any AML with account_id=False",
        )
        self.assertFalse(
            move_lines.filtered(
                lambda l: l.account_id
                in (f["nogate_usage_debit"] + f["nogate_usage_credit"])
            ),
            "A rule without a fixed-account gate must not journal, even when usage resolves",
        )
