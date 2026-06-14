# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestHrPayslip(YamlTransactionCase):
    def test_hr_payslip(self):
        self.run_yaml_scenario("test_data_hr_payslip.yaml")

    def test_onchange_analytic_account_id_set_from_type(self):
        """Setting type_id with analytic account should populate analytic_account_id."""
        analytic = self.env["account.analytic.account"].create(
            {"name": "Test OC Analytic"}
        )
        journal = self.env["account.journal"].create(
            {"name": "Test OC Payroll Journal", "code": "TOCJOC", "type": "general"}
        )
        payslip_type = self.env["hr.payslip_type"].create(
            {
                "name": "Test OC Payslip Type",
                "code": "TOCPSTOC",
                "journal_id": journal.id,
                "analytic_account_id": analytic.id,
            }
        )
        rule_cat = self.env["hr.salary_rule_category"].create(
            {"name": "Test OC Cat", "code": "TOCCATOC"}
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "Test OC Rule",
                "code": "TOCRULEOC",
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        structure = self.env["hr.salary_structure"].create(
            {
                "name": "Test OC Structure",
                "code": "TOCSTROC",
                "rule_ids": [(4, rule.id)],
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Test OC Employee", "salary_structure_id": structure.id}
        )
        form = Form(self.env["hr.payslip"])
        form.employee_id = employee
        form.type_id = payslip_type
        self.assertTrue(form.analytic_account_id)
        self.assertEqual(form.analytic_account_id.id, analytic.id)

    def test_onchange_analytic_account_id_cleared_when_type_changes(self):
        """Changing type_id to one without analytic account should clear analytic_account_id."""
        analytic = self.env["account.analytic.account"].create(
            {"name": "Test OC Analytic Clear"}
        )
        journal = self.env["account.journal"].create(
            {"name": "Test OC Journal Clear", "code": "TOCJCL", "type": "general"}
        )
        payslip_type_with = self.env["hr.payslip_type"].create(
            {
                "name": "Test OC Type With Analytic",
                "code": "TOCPSTWITH",
                "journal_id": journal.id,
                "analytic_account_id": analytic.id,
            }
        )
        payslip_type_without = self.env["hr.payslip_type"].create(
            {
                "name": "Test OC Type Without Analytic",
                "code": "TOCPSTWOUT",
                "journal_id": journal.id,
            }
        )
        rule_cat = self.env["hr.salary_rule_category"].create(
            {"name": "Test OC Cat Clear", "code": "TOCCATCL"}
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "Test OC Rule Clear",
                "code": "TOCRULECL",
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        structure = self.env["hr.salary_structure"].create(
            {
                "name": "Test OC Structure Clear",
                "code": "TOCSTRCL",
                "rule_ids": [(4, rule.id)],
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Test OC Employee Clear", "salary_structure_id": structure.id}
        )
        form = Form(self.env["hr.payslip"])
        form.employee_id = employee
        form.type_id = payslip_type_with
        self.assertTrue(form.analytic_account_id)
        form.type_id = payslip_type_without
        self.assertFalse(form.analytic_account_id)
