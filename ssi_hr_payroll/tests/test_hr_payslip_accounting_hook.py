# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrPayslipAccountingHook(YamlTransactionCase):
    """Test 16: _need_accounting_entry() hook default behaviour."""

    def test_need_accounting_entry_default_true(self):
        """Return ``True`` by default for a standalone payslip.

        Pure Python — trigger P1 (L-01: ``action: call`` discards the
        method's return value; L-02: an assert's actual side is always
        a dotted ``getattr`` on a registry record, so a bare boolean
        return value cannot be asserted from YAML).
        """
        payslip = self.env["hr.payslip"].new(
            {"date_start": "2026-01-01", "date_end": "2026-01-31"}
        )
        self.assertTrue(payslip._need_accounting_entry())
