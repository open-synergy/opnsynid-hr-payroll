# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrPayslip(models.Model):
    """
    Extends hr.payslip with operating unit support.
    Adds mixin.single_operating_unit so payslip documents
    can be scoped to a specific operating unit.
    Overrides _prepare_account_move_data to propagate operating_unit_id
    to the generated accounting entry.
    """

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "mixin.single_operating_unit",
    ]

    def _prepare_account_move_data(self):
        """Add ``operating_unit_id`` to the ``account.move`` values.

        Overridden so the accounting entry generated for this payslip
        is scoped to the same operating unit as the payslip itself.

        :return: dict of ``account.move`` values
        """
        res = super()._prepare_account_move_data()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
