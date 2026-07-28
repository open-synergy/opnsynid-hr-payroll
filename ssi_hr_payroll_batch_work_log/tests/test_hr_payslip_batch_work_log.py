# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchWorkLog(YamlTransactionCase):
    """Run the work log YAML scenario for ``hr.payslip_batch``."""

    def test_hr_payslip_batch_work_log(self):
        """Test the Work Log tab scenario described in the YAML file."""
        self.run_yaml_scenario("test_data_hr_payslip_batch_work_log.yaml")
