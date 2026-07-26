# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrSalaryRuleCategory(models.Model):
    """
    Groups salary rules for subtotal aggregation on a payslip.

    Categories can be nested through ``parent_id``; when a payslip is
    computed, the amount of a rule is added to its own category and
    to every ancestor category, exposed as the ``categories`` local
    variable available to salary rule Python code.
    """

    _name = "hr.salary_rule_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Salary Rule Category"

    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="hr.salary_rule_category",
        ondelete="restrict",
    )
    child_ids = fields.One2many(
        string="Children",
        comodel_name="hr.salary_rule_category",
        inverse_name="parent_id",
    )

    @api.constrains("parent_id")
    def _check_parent_id(self):
        """Forbid a salary rule category from being its own ancestor.

        :raises ValidationError: if ``parent_id`` closes a cycle in
            the category hierarchy.
        """
        if not self._check_recursion():
            raise ValidationError(
                _(
                    "Error! You cannot create recursive hierarchy of Salary "
                    "Rule Category."
                )
            )
