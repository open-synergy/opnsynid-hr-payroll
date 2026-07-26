# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchM2OConfigurator(YamlTransactionCase):
    """Tests the allowed-record fields a batch derives from its type."""

    def test_hr_payslip_batch_m2o_configurator(self):
        """Runs the allowed analytic, usage and employee list scenarios."""
        self.run_yaml_scenario("test_data_hr_payslip_batch_m2o_configurator.yaml")
