# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipLineAccountResolution(TransactionCase):
    """Regression tests for double-journaling bug in payslip line account resolution.

    The fix only blocks usage resolution when the rule is *asymmetric* — i.e. it has
    one side's account set but not the other.  When the rule has neither fixed account,
    usage is still the sole source for both sides (full-usage mode).

    Scenario that triggered the bug (SGRS): two paired rules:
      - Rule A (debit-only): debit_account_id=736, credit_account_id=False
      - Rule B (credit-only): debit_account_id=False, credit_account_id=568
    Before the fix, usage injected a credit AML for Rule A and a debit AML for Rule B,
    so the expense account was debited twice instead of once.
    """

    def setUp(self):
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
        account_usage = self.env["account.account"].create(
            {
                "name": "Test Line Resolution Usage",
                "code": "TSLRUS01",
                "user_type_id": expense_type.id,
            }
        )

        # Usage type: any product + code "TSLRUSE" resolves to account_usage
        # via the fallback chain in _get_product_account().
        self.usage = self.env["product.usage_type"].create(
            {
                "name": "Test Line Resolution Usage Type",
                "code": "TSLRUSE",
                "account_id": account_usage.id,
            }
        )

        # Minimal product without product-specific account mapping so that
        # _get_product_account() falls through to the usage type's own account.
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

        # Create payslip with debit_usage_id and credit_usage_id explicitly set,
        # simulating a payslip type that uses usage-based account resolution.
        admin = self.env.ref("base.user_admin")
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

    def test_usage_resolves_account_via_fallback(self):
        """Sanity: _get_account_by_product_usage returns the usage type account."""
        account = self.product._get_product_account(self.usage.code)
        self.assertTrue(account)

    def test_debit_only_rule_returns_false_for_credit_even_when_usage_resolves(self):
        """Regression: credit must be False when rule has no credit_account_id.

        Proves that usage resolution is blocked by the guard in _get_credit_account()
        even when _get_account_by_product_usage() would successfully return an account.
        """
        # Verify usage CAN resolve an account — confirming the guard is the blocker.
        usage_account = self.line_debit_only._get_account_by_product_usage(
            self.payslip.credit_usage_id
        )
        self.assertTrue(
            usage_account, "Usage should resolve an account for this product"
        )

        # The fix: _get_credit_account() must return False because credit_account_id
        # is not set on the rule, regardless of what usage resolves.
        result = self.line_debit_only._get_credit_account()
        self.assertFalse(
            result,
            "_get_credit_account() must return False when rule has no credit_account_id",
        )

    def test_debit_only_rule_returns_account_for_debit(self):
        """Positive: _get_debit_account() returns an account when debit_account_id is set."""
        result = self.line_debit_only._get_debit_account()
        self.assertTrue(result)

    def test_credit_only_rule_returns_false_for_debit_even_when_usage_resolves(self):
        """Regression: debit must be False when rule has no debit_account_id.

        Proves that usage resolution is blocked by the guard in _get_debit_account()
        even when _get_account_by_product_usage() would successfully return an account.
        """
        # Verify usage CAN resolve an account — confirming the guard is the blocker.
        usage_account = self.line_credit_only._get_account_by_product_usage(
            self.payslip.debit_usage_id
        )
        self.assertTrue(
            usage_account, "Usage should resolve an account for this product"
        )

        # The fix: _get_debit_account() must return False because debit_account_id
        # is not set on the rule, regardless of what usage resolves.
        result = self.line_credit_only._get_debit_account()
        self.assertFalse(
            result,
            "_get_debit_account() must return False when rule has no debit_account_id",
        )

    def test_credit_only_rule_returns_account_for_credit(self):
        """Positive: _get_credit_account() returns an account when credit_account_id is set."""
        result = self.line_credit_only._get_credit_account()
        self.assertTrue(result)

    def test_no_fixed_account_rule_resolves_debit_via_usage(self):
        """Full-usage mode: rule with no fixed accounts can still resolve debit via usage."""
        result = self.line_usage_only._get_debit_account()
        self.assertTrue(
            result,
            "_get_debit_account() must resolve via usage when rule has no fixed accounts",
        )

    def test_no_fixed_account_rule_resolves_credit_via_usage(self):
        """Full-usage mode: rule with no fixed accounts can still resolve credit via usage."""
        result = self.line_usage_only._get_credit_account()
        self.assertTrue(
            result,
            "_get_credit_account() must resolve via usage when rule has no fixed accounts",
        )
