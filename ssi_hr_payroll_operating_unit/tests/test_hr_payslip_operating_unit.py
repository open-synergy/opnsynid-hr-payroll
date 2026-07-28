# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipOperatingUnit(YamlTransactionCase):
    """Tests that a payslip propagates its operating unit to the move."""

    def test_hr_payslip_operating_unit(self):
        """Confirm the generated ``account.move`` keeps the payslip's OU."""
        self.run_yaml_scenario("test_data_hr_payslip_operating_unit.yaml")
        payslip = self.registry.get("payslip")
        self.assertTrue(payslip, "Payslip should be in registry after scenario")
        self.assertTrue(payslip.move_id, "Payslip should have an accounting entry")
        self.assertEqual(
            payslip.move_id.operating_unit_id,
            payslip.operating_unit_id,
            "account.move should have the same operating_unit_id as the payslip",
        )
