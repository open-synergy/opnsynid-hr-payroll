# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrEmployeeInput(YamlTransactionCase):
    """Test suite for the ``hr.employee_input`` detail model."""

    def test_hr_employee_input(self):
        """Run the ``onchange_amount`` scenarios for ``hr.employee_input``."""
        self.run_yaml_scenario("test_data_hr_employee_input.yaml")
