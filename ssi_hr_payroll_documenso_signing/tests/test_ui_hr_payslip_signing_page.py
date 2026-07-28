# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipSigningPage(HttpSavepointCase):
    """UI tour test for the payslip Documenso signing page."""

    @classmethod
    def setUpClass(cls):
        """Grant the payslip validator group to admin for the tour."""
        super().setUpClass()
        # Pre-Condition: the Payslips menu and the create (New) button are gated
        # by the payslip access groups. Granting the validator group to admin
        # implies the user and viewer groups (see ssi_hr_payroll security), so
        # admin can open the Payslips menu and open the create form. Without it
        # the tour would fail on the very first menu step or find no New button.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

    def test_signing_page(self):
        """IK: docs/hr_payslip/01-create.md (E2a delta — Modified Flow)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_documenso_signing_hr_payslip_signing_page",
            login="admin",
        )
