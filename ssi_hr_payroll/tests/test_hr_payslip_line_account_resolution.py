# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipLineAccountResolution(TransactionCase):
    """Tests for payslip line account resolution (_get_debit_account / _get_credit_account).

    Design rule (confirmed by user) — fixed account is a per-side GATE:
      - Debit: rule.debit_account_id is the gate. If empty → no debit line at all,
        even when usage could resolve. If set: when payslip.debit_usage_id is filled,
        resolve the account via usage (falling back to debit_account_id when usage
        cannot resolve); when no usage is filled, use debit_account_id directly.
      - Credit: symmetric with rule.credit_account_id + payslip.credit_usage_id.
      - Consequence: a rule with no fixed account on a side never journals that side;
        usage only OVERRIDES which account is used when the gate is present.
    """

    def setUp(self):
        """Build accounts, usage types, rules, and payslips for the tests."""
        super().setUp()
        expense_type = self.env.ref("account.data_account_type_expenses")

        self.account_debit = self.env["account.account"].create(
            {
                "name": "Test Line Resolution Debit",
                "code": "TSLRDB01",
                "user_type_id": expense_type.id,
            }
        )
        self.account_credit = self.env["account.account"].create(
            {
                "name": "Test Line Resolution Credit",
                "code": "TSLRCR01",
                "user_type_id": expense_type.id,
            }
        )
        self.account_usage = self.env["account.account"].create(
            {
                "name": "Test Line Resolution Usage",
                "code": "TSLRUS01",
                "user_type_id": expense_type.id,
            }
        )

        # Usage type that RESOLVES: falls through to usage_type.account_id.
        self.usage = self.env["product.usage_type"].create(
            {
                "name": "Test Line Resolution Usage Type",
                "code": "TSLRUSE",
                "account_id": self.account_usage.id,
            }
        )

        # Usage type that does NOT resolve: no account_id, no product mapping.
        # _get_product_account("TSLREMPTY") returns False for our product.
        self.usage_no_account = self.env["product.usage_type"].create(
            {
                "name": "Test Line Resolution Empty Usage",
                "code": "TSLREMPTY",
            }
        )

        # Minimal product: no product.account record, so resolution falls through
        # to usage_type.account_id (which is why self.usage resolves but
        # self.usage_no_account does not).
        product_tmpl = self.env["product.template"].create(
            {
                "name": "Test Line Resolution Product",
                "type": "service",
            }
        )
        self.product = product_tmpl.product_variant_ids[0]

        rule_cat = self.env["hr.salary_rule_category"].create(
            {
                "name": "Test Line Resolution Cat",
                "code": "TSLRCAT",
            }
        )

        # Rule with NO fixed accounts — relies entirely on usage for both sides.
        self.rule_usage_only = self.env["hr.salary_rule"].create(
            {
                "name": "Test Line Resolution Usage Only",
                "code": "TSLRUSEONLY",
                "category_id": rule_cat.id,
                "product_id": self.product.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 5,
            }
        )

        # Rule with ONLY debit_account_id — credit_account_id intentionally absent.
        self.rule_debit_only = self.env["hr.salary_rule"].create(
            {
                "name": "Test Line Resolution Debit Only",
                "code": "TSLRDBONLY",
                "category_id": rule_cat.id,
                "debit_account_id": self.account_debit.id,
                "product_id": self.product.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )

        # Rule with ONLY credit_account_id — debit_account_id intentionally absent.
        self.rule_credit_only = self.env["hr.salary_rule"].create(
            {
                "name": "Test Line Resolution Credit Only",
                "code": "TSLRCRONLY",
                "category_id": rule_cat.id,
                "credit_account_id": self.account_credit.id,
                "product_id": self.product.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 20,
            }
        )

        structure = self.env["hr.salary_structure"].create(
            {
                "name": "Test Line Resolution Structure",
                "code": "TSLRSTR",
                "rule_ids": [
                    (4, self.rule_usage_only.id),
                    (4, self.rule_debit_only.id),
                    (4, self.rule_credit_only.id),
                ],
            }
        )

        employee = self.env["hr.employee"].create(
            {
                "name": "Test Line Resolution Employee",
                "salary_structure_id": structure.id,
            }
        )

        journal = self.env["account.journal"].create(
            {
                "name": "Test Line Resolution Journal",
                "code": "TSLRJRN",
                "type": "general",
            }
        )

        payslip_type = self.env["hr.payslip_type"].create(
            {
                "name": "Test Line Resolution Type",
                "code": "TSLRTYPE",
                "journal_id": journal.id,
            }
        )

        admin = self.env.ref("base.user_admin")

        # Main payslip: both debit_usage_id and credit_usage_id resolve.
        self.payslip = (
            self.env["hr.payslip"]
            .with_user(admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": payslip_type.id,
                    "structure_id": structure.id,
                    "journal_id": journal.id,
                    "date_start": "2024-01-01",
                    "date_end": "2024-01-31",
                    "date": "2024-01-31",
                    "debit_usage_id": self.usage.id,
                    "credit_usage_id": self.usage.id,
                }
            )
        )

        # Payslip with NO usage set on either side.
        self.payslip_no_usage = (
            self.env["hr.payslip"]
            .with_user(admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": payslip_type.id,
                    "structure_id": structure.id,
                    "journal_id": journal.id,
                    "date_start": "2024-02-01",
                    "date_end": "2024-02-28",
                    "date": "2024-02-28",
                }
            )
        )

        # Payslip with usage that cannot resolve any account.
        self.payslip_empty_usage = (
            self.env["hr.payslip"]
            .with_user(admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": payslip_type.id,
                    "structure_id": structure.id,
                    "journal_id": journal.id,
                    "date_start": "2024-03-01",
                    "date_end": "2024-03-31",
                    "date": "2024-03-31",
                    "debit_usage_id": self.usage_no_account.id,
                    "credit_usage_id": self.usage_no_account.id,
                }
            )
        )

        # Lines on main payslip (usage resolves for both sides).
        self.line_usage_only = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": self.rule_usage_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_debit_only = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": self.rule_debit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_credit_only = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": self.rule_credit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )

        # Lines on empty-usage payslip (usage present but does not resolve).
        self.line_debit_only_empty_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_empty_usage.id,
                "rule_id": self.rule_debit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_usage_only_empty_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_empty_usage.id,
                "rule_id": self.rule_usage_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_credit_only_empty_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_empty_usage.id,
                "rule_id": self.rule_credit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )

        # Lines on no-usage payslip (usage not set at all).
        self.line_debit_only_no_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_no_usage.id,
                "rule_id": self.rule_debit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_usage_only_no_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_no_usage.id,
                "rule_id": self.rule_usage_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        self.line_credit_only_no_usage = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip_no_usage.id,
                "rule_id": self.rule_credit_only.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )

    # ------------------------------------------------------------------ #
    #  Sanity                                                              #
    # ------------------------------------------------------------------ #

    def test_usage_resolves_account_via_fallback(self):
        """Sanity: _get_account_by_product_usage returns the usage type account."""
        account = self.product._get_product_account(self.usage.code)
        self.assertTrue(account)

    def test_empty_usage_does_not_resolve(self):
        """Sanity: usage_no_account resolves to False for our product."""
        account = self.product._get_product_account(self.usage_no_account.code)
        self.assertFalse(account)

    # ------------------------------------------------------------------ #
    #  Positive: fixed accounts are returned when usage does not resolve  #
    # ------------------------------------------------------------------ #

    def test_debit_only_rule_returns_account_for_debit(self):
        """Positive: gate present + usage resolves → usage account OVERRIDES fixed.

        rule_debit_only has debit_account_id (gate) and self.payslip has a
        debit_usage_id that resolves to self.account_usage. The usage account must
        win over the fixed debit_account_id.
        """
        result = self.line_debit_only._get_debit_account()
        self.assertEqual(
            result,
            self.account_usage,
            "Usage account must override the fixed debit_account_id when the gate is set",
        )

    def test_credit_only_rule_returns_account_for_credit(self):
        """Positive: gate present + usage resolves → usage account OVERRIDES fixed."""
        result = self.line_credit_only._get_credit_account()
        self.assertEqual(
            result,
            self.account_usage,
            "Usage account must override the fixed credit_account_id when the gate is set",
        )

    # ------------------------------------------------------------------ #
    #  Gate semantics: no fixed account on a side → no line for that side, #
    #  even when usage could resolve (new design)                          #
    # ------------------------------------------------------------------ #

    def test_no_fixed_account_rule_returns_false_for_debit_even_when_usage_resolves(
        self,
    ):
        """Gate empty: rule without debit_account_id → no debit line, despite usage."""
        usage_account = self.line_usage_only._get_account_by_product_usage(
            self.payslip.debit_usage_id
        )
        self.assertTrue(usage_account, "Precondition: usage must resolve an account")

        result = self.line_usage_only._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False when the rule has no "
            "debit_account_id gate, even if usage resolves",
        )

    def test_no_fixed_account_rule_returns_false_for_credit_even_when_usage_resolves(
        self,
    ):
        """Gate empty: rule without credit_account_id → no credit line, despite usage."""
        usage_account = self.line_usage_only._get_account_by_product_usage(
            self.payslip.credit_usage_id
        )
        self.assertTrue(usage_account, "Precondition: usage must resolve an account")

        result = self.line_usage_only._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False when the rule has no "
            "credit_account_id gate, even if usage resolves",
        )

    # ------------------------------------------------------------------ #
    #  Cross-side: the opposite side's gate is empty → no line for that    #
    #  side, even when usage could resolve (gate replaces the old guard)   #
    # ------------------------------------------------------------------ #

    def test_debit_only_rule_returns_false_for_credit_without_gate(self):
        """Gate empty on credit side: debit-only rule (credit_account_id=False) must
        NOT obtain a credit account via usage."""
        usage_account = self.line_debit_only._get_account_by_product_usage(
            self.payslip.credit_usage_id
        )
        self.assertTrue(usage_account, "Precondition: usage must resolve an account")

        result = self.line_debit_only._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False for a debit-only rule: the "
            "credit_account_id gate is empty, so usage is ignored",
        )

    def test_credit_only_rule_returns_false_for_debit_without_gate(self):
        """Gate empty on debit side: credit-only rule (debit_account_id=False) must
        NOT obtain a debit account via usage."""
        usage_account = self.line_credit_only._get_account_by_product_usage(
            self.payslip.debit_usage_id
        )
        self.assertTrue(usage_account, "Precondition: usage must resolve an account")

        result = self.line_credit_only._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False for a credit-only rule: the "
            "debit_account_id gate is empty, so usage is ignored",
        )

    # ------------------------------------------------------------------ #
    #  Fallback matrix — DEBIT side                                        #
    # ------------------------------------------------------------------ #

    def test_fallback_debit_usage_no_resolve_has_fixed_returns_fixed(self):
        """Debit fallback: usage present but unresolvable → falls to debit_account_id."""
        result = self.line_debit_only_empty_usage._get_debit_account()
        self.assertEqual(
            result,
            self.account_debit,
            "Must fall back to rule.debit_account_id when usage cannot resolve",
        )

    def test_fallback_debit_usage_no_resolve_no_fixed_returns_false(self):
        """Debit fallback: usage present but unresolvable + no fixed → False."""
        result = self.line_usage_only_empty_usage._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False when neither usage nor fixed resolves",
        )

    def test_fallback_debit_no_usage_has_fixed_returns_fixed(self):
        """Debit fallback: no usage set → falls to debit_account_id."""
        result = self.line_debit_only_no_usage._get_debit_account()
        self.assertEqual(
            result,
            self.account_debit,
            "Must return rule.debit_account_id when no usage is set on the payslip",
        )

    def test_fallback_debit_no_usage_no_fixed_returns_false(self):
        """Debit fallback: no usage set + no fixed account → False."""
        result = self.line_usage_only_no_usage._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False when no usage and no fixed account",
        )

    def test_fallback_debit_no_product_usage_present_has_fixed_returns_fixed(self):
        """Debit fallback: rule has no product_id → usage skipped → falls to fixed."""
        rule_cat = self.env["hr.salary_rule_category"].search(
            [("code", "=", "TSLRCAT")], limit=1
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "No Product Debit Only",
                "code": "TSLRNPDB01",
                "category_id": rule_cat.id,
                "debit_account_id": self.account_debit.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 99,
            }
        )
        line = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": rule.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        result = line._get_debit_account()
        self.assertEqual(
            result,
            self.account_debit,
            "Must return rule.debit_account_id when rule has no product_id",
        )

    def test_fallback_debit_no_product_no_fixed_returns_false(self):
        """Debit fallback: rule has no product_id + no fixed account → False."""
        rule_cat = self.env["hr.salary_rule_category"].search(
            [("code", "=", "TSLRCAT")], limit=1
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "No Product No Fixed",
                "code": "TSLRNPNF01",
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 99,
            }
        )
        line = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": rule.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        result = line._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False when no product_id and no fixed account",
        )

    # ------------------------------------------------------------------ #
    #  Fallback matrix — CREDIT side (symmetric)                           #
    # ------------------------------------------------------------------ #

    def test_fallback_credit_usage_no_resolve_has_fixed_returns_fixed(self):
        """Credit fallback: usage present but unresolvable → falls to credit_account_id."""
        result = self.line_credit_only_empty_usage._get_credit_account()
        self.assertEqual(
            result,
            self.account_credit,
            "Must fall back to rule.credit_account_id when usage cannot resolve",
        )

    def test_fallback_credit_usage_no_resolve_no_fixed_returns_false(self):
        """Credit fallback: usage present but unresolvable + no fixed → False."""
        result = self.line_usage_only_empty_usage._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False when neither usage nor fixed resolves",
        )

    def test_fallback_credit_no_usage_has_fixed_returns_fixed(self):
        """Credit fallback: no usage set → falls to credit_account_id."""
        result = self.line_credit_only_no_usage._get_credit_account()
        self.assertEqual(
            result,
            self.account_credit,
            "Must return rule.credit_account_id when no usage is set on the payslip",
        )

    def test_fallback_credit_no_usage_no_fixed_returns_false(self):
        """Credit fallback: no usage set + no fixed account → False."""
        result = self.line_usage_only_no_usage._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False when no usage and no fixed account",
        )

    def test_fallback_credit_no_product_usage_present_has_fixed_returns_fixed(self):
        """Credit fallback: rule has no product_id → usage skipped → falls to fixed."""
        rule_cat = self.env["hr.salary_rule_category"].search(
            [("code", "=", "TSLRCAT")], limit=1
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "No Product Credit Only",
                "code": "TSLRNPCR01",
                "category_id": rule_cat.id,
                "credit_account_id": self.account_credit.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 99,
            }
        )
        line = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": rule.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        result = line._get_credit_account()
        self.assertEqual(
            result,
            self.account_credit,
            "Must return rule.credit_account_id when rule has no product_id",
        )

    def test_fallback_credit_no_product_no_fixed_returns_false(self):
        """Credit fallback: rule has no product_id + no fixed account → False."""
        rule_cat = self.env["hr.salary_rule_category"].search(
            [("code", "=", "TSLRCAT")], limit=1
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "No Product No Fixed Credit",
                "code": "TSLRNPNFC01",
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 99,
            }
        )
        line = self.env["hr.payslip_line"].create(
            {
                "payslip_id": self.payslip.id,
                "rule_id": rule.id,
                "amount": 100.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        result = line._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False when no product_id and no fixed account",
        )
