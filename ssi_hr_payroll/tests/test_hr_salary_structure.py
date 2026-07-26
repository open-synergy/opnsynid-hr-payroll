# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrSalaryStructure(YamlTransactionCase):
    """Test suite for the ``hr.salary_structure`` master data model."""

    def test_hr_salary_structure(self):
        """Run the scenario creating a simple structure with one rule."""
        self.run_yaml_scenario("test_data_hr_salary_structure.yaml")
