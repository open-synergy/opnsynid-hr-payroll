# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchSummaryReport(YamlTransactionCase):
    """Test the Salary Summary report values and XLSX generation."""

    @classmethod
    def setUpClass(cls):
        """Create rules, structure, employee, batch and payslip fixtures."""
        super().setUpClass()

        # Salary rule category
        cls.rule_cat = cls.env["hr.salary_rule_category"].create(
            {"name": "SR Report Test Cat", "code": "SRRTCAT"}
        )

        # Two salary rules with different sequences
        cls.rule_a = cls.env["hr.salary_rule"].create(
            {
                "name": "SR Report Rule A",
                "code": "SRRTA",
                "category_id": cls.rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 500000.0",
                "sequence": 10,
            }
        )
        cls.rule_b = cls.env["hr.salary_rule"].create(
            {
                "name": "SR Report Rule B",
                "code": "SRRTB",
                "category_id": cls.rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 250000.0",
                "sequence": 20,
            }
        )

        # Salary structure
        cls.structure = cls.env["hr.salary_structure"].create(
            {
                "name": "SR Report Structure",
                "code": "SRRTSTR",
                "rule_ids": [(4, cls.rule_a.id), (4, cls.rule_b.id)],
            }
        )

        # Journal
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "SR Report Payroll Journal",
                "code": "SRRTJRN",
                "type": "general",
            }
        )

        # Payslip type
        cls.payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "SR Report Payslip Type",
                "code": "SRRTTYPE",
                "journal_id": cls.journal.id,
            }
        )

        # Employee
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "SR Report Employee",
                "salary_structure_id": cls.structure.id,
            }
        )

        # Payslip batch
        cls.batch = cls.env["hr.payslip_batch"].create(
            {
                "type_id": cls.payslip_type.id,
                "date_start": "2024-09-01",
                "date_end": "2024-09-30",
                "date": "2024-09-30",
                "employee_ids": [(4, cls.employee.id)],
            }
        )

        # Payslip linked to batch
        cls.payslip = cls.env["hr.payslip"].create(
            {
                "employee_id": cls.employee.id,
                "type_id": cls.payslip_type.id,
                "structure_id": cls.structure.id,
                "journal_id": cls.journal.id,
                "date_start": "2024-09-01",
                "date_end": "2024-09-30",
                "date": "2024-09-30",
                "batch_id": cls.batch.id,
            }
        )

        # Create payslip lines directly (bypassing computation engine)
        cls.env["hr.payslip_line"].create(
            {
                "payslip_id": cls.payslip.id,
                "rule_id": cls.rule_a.id,
                "amount": 500000.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )
        cls.env["hr.payslip_line"].create(
            {
                "payslip_id": cls.payslip.id,
                "rule_id": cls.rule_b.id,
                "amount": 250000.0,
                "quantity": 1.0,
                "rate": 100.0,
            }
        )

        cls.report_obj = cls.env[
            "report.ssi_hr_payroll_batch_summary_report.batch_summary"
        ]

    def test_get_salary_rules_returns_sorted_by_sequence(self):
        """Assert ``_get_salary_rules`` orders rules by sequence.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare recordset return value).
        """
        rules = self.report_obj._get_salary_rules(self.batch)
        rule_ids = rules.ids
        self.assertIn(self.rule_a.id, rule_ids)
        self.assertIn(self.rule_b.id, rule_ids)
        self.assertLess(
            rule_ids.index(self.rule_a.id),
            rule_ids.index(self.rule_b.id),
        )

    def test_get_salary_rules_empty_batch(self):
        """Assert ``_get_salary_rules`` returns empty for empty batch.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare recordset return value).
        """
        empty_batch = self.env["hr.payslip_batch"].create(
            {
                "type_id": self.payslip_type.id,
                "date_start": "2024-10-01",
                "date_end": "2024-10-31",
                "date": "2024-10-31",
            }
        )
        rules = self.report_obj._get_salary_rules(empty_batch)
        self.assertFalse(rules)

    def test_get_amounts_by_rule(self):
        """Assert ``_get_amounts_by_rule`` maps rule id to its total.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).
        """
        amounts = self.report_obj._get_amounts_by_rule(self.payslip)
        self.assertIn(self.rule_a.id, amounts)
        self.assertIn(self.rule_b.id, amounts)
        self.assertAlmostEqual(amounts[self.rule_a.id], 500000.0)
        self.assertAlmostEqual(amounts[self.rule_b.id], 250000.0)

    def test_fmt_positive_number(self):
        """Assert ``_fmt`` formats a positive number with dot groups.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare string return value).
        """
        result = self.report_obj._fmt(1234567)
        self.assertEqual(result, "1.234.567")

    def test_fmt_zero(self):
        """Assert ``_fmt`` formats zero correctly.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare string return value).
        """
        result = self.report_obj._fmt(0)
        self.assertEqual(result, "0")

    def test_fmt_negative_number(self):
        """Assert ``_fmt`` formats negative numbers with a minus sign.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare string return value).
        """
        result = self.report_obj._fmt(-500000)
        self.assertEqual(result, "-500.000")

    def test_get_report_values_structure(self):
        """Assert ``_get_report_values`` returns docs with all keys.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).
        """
        report_values = self.report_obj._get_report_values([self.batch.id])

        self.assertIn("docs", report_values)
        self.assertEqual(len(report_values["docs"]), 1)

        doc = report_values["docs"][0]
        self.assertIn("batch", doc)
        self.assertIn("rules", doc)
        self.assertIn("payslips", doc)
        self.assertIn("rule_totals", doc)
        self.assertIn("rule_totals_fmt", doc)
        self.assertIn("grand_total", doc)
        self.assertIn("grand_total_fmt", doc)

    def test_get_report_values_totals(self):
        """Assert ``_get_report_values`` computes per-rule and grand total.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).
        """
        report_values = self.report_obj._get_report_values([self.batch.id])
        doc = report_values["docs"][0]

        self.assertAlmostEqual(doc["rule_totals"][self.rule_a.id], 500000.0)
        self.assertAlmostEqual(doc["rule_totals"][self.rule_b.id], 250000.0)
        self.assertAlmostEqual(doc["grand_total"], 750000.0)

    def test_get_report_values_payslip_row(self):
        """Assert ``_get_report_values`` includes a formatted payslip row.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).
        """
        report_values = self.report_obj._get_report_values([self.batch.id])
        doc = report_values["docs"][0]

        self.assertEqual(len(doc["payslips"]), 1)
        row = doc["payslips"][0]
        self.assertEqual(row["no"], 1)
        self.assertIn("payslip", row)
        self.assertIn("amounts_fmt", row)
        self.assertIn("total_fmt", row)
        self.assertEqual(row["total_fmt"], "750.000")

    def test_xlsx_report_generates_file(self):
        """Assert ``create_xlsx_report`` produces a non-empty XLSX file.

        Pure Python — trigger P8 (L-01: ``call`` discards the method
        return value, so the rendered bytes can't be asserted from
        YAML; L-19: the base class is locked to ``TransactionCase``,
        so report rendering can't reach an ``HttpCase``-only helper).
        """
        report_xlsx = self.env[
            "report.ssi_hr_payroll_batch_summary_report.batch_summary_xlsx"
        ].with_context(active_model="hr.payslip_batch")
        content, content_type = report_xlsx.create_xlsx_report([self.batch.id], {})
        self.assertEqual(content_type, "xlsx")
        self.assertTrue(content)

    def test_xlsx_report_with_analytic_account(self):
        """Assert XLSX generation handles a batch with an analytic account.

        Pure Python — trigger P8 (L-01: ``call`` discards the method
        return value, so the rendered bytes can't be asserted from
        YAML; L-19: the base class is locked to ``TransactionCase``,
        so report rendering can't reach an ``HttpCase``-only helper).
        """
        analytic = self.env["account.analytic.account"].create(
            {"name": "SR Report Analytic"}
        )
        self.batch.analytic_account_id = analytic.id
        report_xlsx = self.env[
            "report.ssi_hr_payroll_batch_summary_report.batch_summary_xlsx"
        ].with_context(active_model="hr.payslip_batch")
        content, content_type = report_xlsx.create_xlsx_report([self.batch.id], {})
        self.assertEqual(content_type, "xlsx")
        self.assertTrue(content)
        self.batch.analytic_account_id = False

    def test_action_print_salary_summary_returns_action(self):
        """Assert ``action_print_salary_summary`` returns a report action.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).

        ``discard_logo_check`` prevents Odoo from redirecting to the
        document layout configurator when ``external_report_layout_id``
        is unset (CI env).
        """
        action = self.batch.with_context(
            discard_logo_check=True
        ).action_print_salary_summary()
        self.assertIsInstance(action, dict)
        self.assertEqual(action.get("type"), "ir.actions.report")

    def test_action_export_salary_summary_xlsx_returns_action(self):
        """Assert ``action_export_salary_summary_xlsx`` returns an action.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare dict return value).
        """
        action = self.batch.with_context(
            discard_logo_check=True
        ).action_export_salary_summary_xlsx()
        self.assertIsInstance(action, dict)
        self.assertEqual(action.get("type"), "ir.actions.report")
