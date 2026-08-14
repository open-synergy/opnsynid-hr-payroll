# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipLock(YamlTransactionCase):
    """Tests the batch lock guarding ``hr.payslip.action_done``."""

    def test_hr_payslip_lock(self):
        """Run the YAML done transition and batch lock scenario.

        Covers an unbatched payslip reaching ``done`` through its own
        action methods, a batched payslip refusing ``action_done``
        without the ``from_batch`` context key, and that same payslip
        reaching ``done`` once the key is supplied.
        """
        self.run_yaml_scenario("test_data_hr_payslip_lock.yaml")
