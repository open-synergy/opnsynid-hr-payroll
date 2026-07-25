# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipM2OConfigurator(YamlTransactionCase):
    def test_hr_payslip_m2o_configurator(self):
        self.run_yaml_scenario("test_data_hr_payslip_m2o_configurator.yaml")
