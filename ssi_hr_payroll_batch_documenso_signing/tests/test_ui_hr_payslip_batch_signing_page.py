# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatchSigningPage(HttpSavepointCase):
    """Tour: the Documenso signing page/tab is reachable from the
    payslip batch form (IK 01-create.md, E2a delta)."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the validator group so the tour's menu and
        create (New) button steps are reachable."""
        super().setUpClass()
        # Pre-Condition: the Payslip Batches menu and the create (New) button are
        # gated by the payslip batch access groups. Granting the validator group
        # to admin implies the user and viewer groups (see ssi_hr_payroll_batch
        # security), so admin can open the Payslip Batches menu and open the
        # create form. Without it the tour would fail on the very first menu step
        # or find no New button.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_validator_group"
        ).sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

    def test_signing_page(self):
        """IK: docs/hr_payslip_batch/01-create.md (E2a delta — Modified Flow)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_documenso_signing_hr_payslip_batch_signing_page",
            login="admin",
        )
