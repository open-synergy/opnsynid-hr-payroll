# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrPayslip(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends hr.payslip with operating unit support.
    Adds mixin.single_operating_unit so payslip documents
    can be scoped to a specific operating unit.
    """

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "mixin.single_operating_unit",
    ]
