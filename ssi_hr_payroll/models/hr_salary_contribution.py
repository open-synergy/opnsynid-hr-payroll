# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrSalaryContribution(models.Model):
    """
    Represents a third-party contribution scheme referenced by rules.

    Links a ``res.partner`` (e.g. an insurer or government agency)
    that receives the payment when a ``hr.salary_rule`` posts to this
    contribution; the partner drives
    ``hr.payslip_line._get_partner_id``.
    """

    _name = "hr.salary_contribution"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Salary Contribution"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        ondelete="restrict",
    )
