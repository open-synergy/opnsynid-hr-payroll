# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipBatchMulti(YamlTransactionCase):
    """Tests ``hr.payslip_batch`` transitions on multi-record sets."""

    def test_hr_payslip_batch_multi(self):
        """Runs confirm, reject, cancel and restart on two batches."""
        self.run_yaml_scenario("test_data_hr_payslip_batch_multi.yaml")
