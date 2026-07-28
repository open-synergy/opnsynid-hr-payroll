# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipWorkLog(YamlTransactionCase):
    """Test the ``mixin.work_object`` inheritance on ``hr.payslip``."""

    def test_hr_payslip_work_log(self):
        """Test creating a payslip lands in ``draft`` with the mixin in."""
        self.run_yaml_scenario("test_data_hr_payslip_work_log.yaml")
