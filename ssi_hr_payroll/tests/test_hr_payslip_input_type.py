# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipInputType(YamlTransactionCase):
    """Test suite for the ``hr.payslip_input_type`` master data model."""

    def test_hr_payslip_input_type(self):
        """Run the create-and-verify scenario for ``hr.payslip_input_type``."""
        self.run_yaml_scenario("test_data_hr_payslip_input_type.yaml")
