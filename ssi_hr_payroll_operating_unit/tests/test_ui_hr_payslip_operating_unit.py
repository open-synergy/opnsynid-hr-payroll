# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipOperatingUnit(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition: the Operating Unit field is gated by the multi operating
        # unit group; without it the field is not rendered and the delta assertion
        # would never find it. The user must also be able to open the Payslips menu
        # and create a payslip, so grant the payslip User group (implies the Viewer
        # group that gates the menu).
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )
        cls.env.ref("ssi_hr_payroll.hr_payslip_user_group").sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

    def test_field_ou(self):
        """IK: docs/hr_payslip/01-create.md (E1 delta — Additional Fields)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_operating_unit_hr_payslip_field_ou",
            login="admin",
        )
