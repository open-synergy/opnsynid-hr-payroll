# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchOperatingUnit(YamlTransactionCase):
    def test_hr_payslip_batch_operating_unit(self):
        self.run_yaml_scenario("test_data_hr_payslip_batch_operating_unit.yaml")

    def _create_salary_structure(self, suffix):
        rule_cat = self.env["hr.salary_rule_category"].create(
            {"name": "OU Reload Test Cat %s" % suffix, "code": "OURLCAT%s" % suffix}
        )
        rule = self.env["hr.salary_rule"].create(
            {
                "name": "OU Reload Test Rule %s" % suffix,
                "code": "OURLRULE%s" % suffix,
                "category_id": rule_cat.id,
                "condition_python": "result = True",
                "amount_python": "result = 100.0",
                "sequence": 10,
            }
        )
        return self.env["hr.salary_structure"].create(
            {
                "name": "OU Reload Test Structure %s" % suffix,
                "code": "OURLSTR%s" % suffix,
                "rule_ids": [(4, rule.id)],
            }
        )

    def test_reload_employee_filters_by_operating_unit(self):
        """action_reload_employee must only load employees whose operating_unit_id
        matches the batch's operating_unit_id."""
        company = self.env.ref("base.main_company")
        partner = self.env.ref("base.main_partner")

        ou1 = self.env["operating.unit"].create(
            {
                "name": "OU Reload Test OU1",
                "code": "OURLTOU1",
                "partner_id": partner.id,
                "company_id": company.id,
            }
        )
        ou2 = self.env["operating.unit"].create(
            {
                "name": "OU Reload Test OU2",
                "code": "OURLTOU2",
                "partner_id": partner.id,
                "company_id": company.id,
            }
        )

        structure = self._create_salary_structure("A")

        employee_ou1 = self.env["hr.employee"].create(
            {
                "name": "OU Reload Test Employee OU1",
                "salary_structure_id": structure.id,
                "operating_unit_id": ou1.id,
            }
        )
        self.env["hr.employee"].create(
            {
                "name": "OU Reload Test Employee OU2",
                "salary_structure_id": structure.id,
                "operating_unit_id": ou2.id,
            }
        )

        journal = self.env["account.journal"].create(
            {
                "name": "OU Reload Test Journal",
                "code": "OURLJ",
                "type": "general",
            }
        )
        payslip_type = self.env["hr.payslip_type"].create(
            {
                "name": "OU Reload Test Type",
                "code": "OURLTYPE",
                "journal_id": journal.id,
            }
        )
        batch = (
            self.env["hr.payslip_batch"]
            .sudo()
            .create(
                {
                    "type_id": payslip_type.id,
                    "date_start": "2024-10-01",
                    "date_end": "2024-10-31",
                    "date": "2024-10-31",
                    "operating_unit_id": ou1.id,
                }
            )
        )

        batch.action_reload_employee()

        self.assertIn(
            employee_ou1,
            batch.employee_ids,
            "Employee with matching OU should be loaded after Reload",
        )
        non_ou1_employees = batch.employee_ids.filtered(
            lambda e: e.operating_unit_id != ou1
        )
        self.assertFalse(
            non_ou1_employees,
            "Employees with different OU must not be loaded after Reload",
        )
