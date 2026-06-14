# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatch(YamlTransactionCase):
    def test_hr_payslip_batch(self):
        self.run_yaml_scenario("test_data_hr_payslip_batch.yaml")

    def test_onchange_analytic_account_id_set_from_type(self):
        """Setting type_id with analytic account should populate analytic_account_id."""
        analytic = self.env["account.analytic.account"].create(
            {"name": "Test Batch OC Analytic"}
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Test Batch OC Journal",
                "code": "TBOCJOC",
                "type": "general",
            }
        )
        payslip_type = self.env["hr.payslip_type"].create(
            {
                "name": "Test Batch OC Type",
                "code": "TBOCTYPE",
                "journal_id": journal.id,
                "analytic_account_id": analytic.id,
            }
        )
        form = Form(self.env["hr.payslip_batch"])
        form.type_id = payslip_type
        self.assertTrue(form.analytic_account_id)
        self.assertEqual(form.analytic_account_id.id, analytic.id)

    def test_onchange_analytic_account_id_cleared_when_type_changes(self):
        """Changing type_id to one without analytic account should clear analytic_account_id."""
        analytic = self.env["account.analytic.account"].create(
            {"name": "Test Batch OC Analytic Clear"}
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Test Batch OC Journal Clear",
                "code": "TBOCJCL",
                "type": "general",
            }
        )
        payslip_type_with = self.env["hr.payslip_type"].create(
            {
                "name": "Test Batch OC Type With Analytic",
                "code": "TBOCTWITH",
                "journal_id": journal.id,
                "analytic_account_id": analytic.id,
            }
        )
        payslip_type_without = self.env["hr.payslip_type"].create(
            {
                "name": "Test Batch OC Type Without Analytic",
                "code": "TBOCT2",
                "journal_id": journal.id,
            }
        )
        form = Form(self.env["hr.payslip_batch"])
        form.type_id = payslip_type_with
        self.assertTrue(form.analytic_account_id)
        form.type_id = payslip_type_without
        self.assertFalse(form.analytic_account_id)

    def test_prepare_payslip_data_includes_analytic_account(self):
        """_prepare_payslip_data must include analytic_account_id from batch."""
        analytic = self.env["account.analytic.account"].create(
            {"name": "Test Batch Propagation Analytic"}
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Test Batch Propagation Journal",
                "code": "TBPRJRN",
                "type": "general",
            }
        )
        rule_cat = self.env["hr.salary_rule_category"].create(
            {"name": "Test Batch Prop Cat", "code": "TBPROPCAT"}
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "Test Batch Prop Rule",
                "code": "TBPROPRULE",
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        structure = self.env["hr.salary_structure"].create(
            {
                "name": "Test Batch Prop Structure",
                "code": "TBPROPSTR",
                "rule_ids": [(4, rule.id)],
            }
        )
        payslip_type = self.env["hr.payslip_type"].create(
            {
                "name": "Test Batch Prop Type",
                "code": "TBPROPTYPE",
                "journal_id": journal.id,
                "analytic_account_id": analytic.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {
                "name": "Test Batch Prop Employee",
                "salary_structure_id": structure.id,
            }
        )
        batch = self.env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "analytic_account_id": analytic.id,
                "date_start": "2024-11-01",
                "date_end": "2024-11-30",
                "date": "2024-11-30",
            }
        )
        payslip_data = batch._prepare_payslip_data(employee)
        self.assertEqual(
            payslip_data.get("analytic_account_id"),
            analytic.id,
        )
