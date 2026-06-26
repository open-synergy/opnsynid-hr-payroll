# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipAccountingHook(TransactionCase):
    """Test 16: _need_accounting_entry() hook default behaviour."""

    def test_need_accounting_entry_default_true(self):
        """_need_accounting_entry() must return True by default (standalone payslip)."""
        payslip = self.env["hr.payslip"].new(
            {"date_start": "2026-01-01", "date_end": "2026-01-31"}
        )
        self.assertTrue(payslip._need_accounting_entry())
