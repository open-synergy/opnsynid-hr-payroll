# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatchOperatingUnit(HttpSavepointCase):
    """Tour test for the Operating Unit field on the payslip batch form."""

    @classmethod
    def setUpClass(cls):
        """Grant the admin user batch and multi-OU access for the tour."""
        super().setUpClass()
        # Pre-Condition: the Operating Unit field on the batch form is gated by the
        # Multi Operating Unit group; without it the server strips the field from the
        # arch and the tour assertion would never match. The batch User group grants
        # the create access needed to open the New form.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_payroll_batch.hr_payslip_batch_user_group").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_field_ou(self):
        """IK: docs/hr_payslip_batch/01-create.md (E1 delta — Operating Unit field)"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_batch_operating_unit_hr_payslip_batch_field_ou",
            login="admin",
        )
