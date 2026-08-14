# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=duplicate-code

from odoo import api, fields, models


class HrPayslipInput(models.Model):  # pylint: disable=too-few-public-methods
    """
    Stores a one-off input amount attached to a single payslip.

    Each line pairs an ``hr.payslip_input_type`` with an ``amount``
    that salary rule Python code can read through the ``inputs``
    local variable while computing that specific payslip.
    """

    _name = "hr.payslip_input"

    _description = "Payslip Input"

    payslip_id = fields.Many2one(
        string="Payslip",
        comodel_name="hr.payslip",
        required=True,
        ondelete="cascade",
    )
    input_type_id = fields.Many2one(
        string="Input Type",
        comodel_name="hr.payslip_input_type",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        default=0.0,
    )

    @api.onchange("input_type_id")
    def onchange_amount(self):
        """Copy the default amount from the selected input type.

        Sets ``amount`` to ``input_type_id.default_amount`` so the
        user starts from the type's usual value instead of ``0.0``.
        """
        if self.input_type_id:
            self.amount = self.input_type_id.default_amount
