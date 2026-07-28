# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchOperatingUnit(YamlTransactionCase):
    """Test hr.payslip_batch operating unit scoping and OU propagation."""

    def test_hr_payslip_batch_operating_unit(self):
        """Run the YAML scenario for OU-scoped payslip batch behavior."""
        self.run_yaml_scenario("test_data_hr_payslip_batch_operating_unit.yaml")

    def _create_salary_structure(self, suffix):
        """Create a minimal salary structure with one flat-rate rule."""
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

        struct_field = (
            "manual_salary_structure_id"
            if "manual_salary_structure_id" in self.env["hr.employee"]._fields
            else "salary_structure_id"
        )
        employee_ou1 = self.env["hr.employee"].create(
            {
                "name": "OU Reload Test Employee OU1",
                struct_field: structure.id,
                "operating_unit_id": ou1.id,
            }
        )
        self.env["hr.employee"].create(
            {
                "name": "OU Reload Test Employee OU2",
                struct_field: structure.id,
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

    def _create_batch_move_ou_fixtures(self, prefix):
        """Return fixtures for testing move operating_unit_id propagation."""
        env = self.env
        company = env.ref("base.main_company")
        partner = env.ref("base.main_partner")
        acc_type = env.ref("account.data_account_type_expenses")

        ou = env["operating.unit"].create(
            {
                "name": "%s OU" % prefix,
                "code": "%sOU" % prefix,
                "partner_id": partner.id,
                "company_id": company.id,
            }
        )
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
        employee = env["hr.employee"].create(
            {
                "name": "%s Employee" % prefix,
                struct_field: structure.id,
                "operating_unit_id": ou.id,
            }
        )
        batch = env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "accounting_method": "batch",
                "journal_id": journal.id,
                "date_start": "2026-05-01",
                "date_end": "2026-05-31",
                "date": "2026-05-31",
                "operating_unit_id": ou.id,
                "employee_ids": [(6, 0, [employee.id])],
            }
        )
        return {"batch": batch, "ou": ou}

    def _run_batch_to_done(self, batch):
        """Drive a batch through the full approval workflow to done state."""
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

    def test_batch_move_has_same_operating_unit_as_batch(self):
        """_prepare_standard_move must propagate operating_unit_id to account.move.

        When accounting_method is 'batch', the journal entry created at done
        must carry the same operating_unit_id as the payslip batch.
        """
        f = self._create_batch_move_ou_fixtures("TMOVOU")
        batch = f["batch"]
        ou = f["ou"]

        self._run_batch_to_done(batch)

        self.assertEqual(batch.state, "done")
        self.assertTrue(
            batch.move_id,
            "Batch with accounting_method=batch must have a move_id after done",
        )
        self.assertEqual(
            batch.move_id.operating_unit_id,
            ou,
            "Journal entry operating_unit_id must match the batch operating_unit_id",
        )
