# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrSalaryRule(HttpSavepointCase):
    """UI tour test suite for the ``hr.salary_rule`` menu."""

    @classmethod
    def setUpClass(cls):
        """Grant configurator group to admin and create a rule category."""
        super().setUpClass()
        # Pre-Condition: the Salary Rules master data menu is gated by the
        # Salary Rule configurator group. Without it the tour would fail on its
        # very first step because the menu is not rendered at all.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_configurator = cls.env.ref(
            "ssi_hr_payroll.hr_salary_rule_configurator_group"
        )
        cls.group_configurator.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )
        # Pre-Condition: the Category field is mandatory, so at least one Salary
        # Rule Category must already exist for the record to be saved. The tour
        # selects this record on the Category field.
        cls.category = cls.env["hr.salary_rule_category"].create(
            {
                "name": "TOUR-CATEGORY-FOR-RULE",
                "code": "TOUR-CFR",
            }
        )

    def test_create(self):
        """IK: docs/hr_salary_rule/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_hr_payroll_hr_salary_rule_create",
            login="admin",
        )
