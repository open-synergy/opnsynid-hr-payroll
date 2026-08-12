# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslip(YamlTransactionCase):
    """Test suite for the ``hr.payslip`` model workflow and accounting."""

    def test_hr_payslip(self):
        """Run the full payslip workflow scenario: draft to done.

        Also covers the ``analytic_account_id`` onchange scenarios
        (set from ``type_id``, cleared when ``type_id`` changes) via
        ``action: form`` steps in the same YAML file.
        """
        self.run_yaml_scenario("test_data_hr_payslip.yaml")
