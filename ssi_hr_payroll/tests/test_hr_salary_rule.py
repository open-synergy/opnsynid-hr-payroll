# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrSalaryRule(YamlTransactionCase):
    """Test suite for the ``hr.salary_rule`` master data model."""

    def test_hr_salary_rule(self):
        """Run the scenario creating a simple rule linked to a category."""
        self.run_yaml_scenario("test_data_hr_salary_rule.yaml")
