# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipInputType(HttpSavepointCase):
    """UI tour test suite for the ``hr.payslip_input_type`` menu."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group to admin so the tour menu renders."""
        super().setUpClass()
        # Pre-Condition: the Input Types master data menu is gated by the
        # Payslip Input Type configurator group. Without it the tour would fail
        # on its very first step because the menu is not rendered at all.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_configurator = cls.env.ref(
            "ssi_hr_payroll.hr_payslip_input_type_configurator_group"
        )
        cls.group_configurator.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

    def test_create(self):
        """IK: docs/hr_payslip_input_type/01-create.md"""
        self.start_tour(
            "/web", "ssi_hr_payroll_hr_payslip_input_type_create", login="admin"
        )
