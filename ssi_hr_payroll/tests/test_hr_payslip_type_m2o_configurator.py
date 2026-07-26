# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipTypeM2OConfigurator(YamlTransactionCase):
    """Test suite for the M2O configurator defaults on ``hr.payslip_type``."""

    def test_hr_payslip_type_m2o_configurator(self):
        """Run the scenario verifying M2O configurator open-domain default."""
        self.run_yaml_scenario("test_data_hr_payslip_type_m2o_configurator.yaml")
