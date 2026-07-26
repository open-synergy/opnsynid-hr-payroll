# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=duplicate-code

from odoo import api, fields, models


class HrEmployeeInput(models.Model):  # pylint: disable=too-few-public-methods
    """
    Stores a recurring payroll input amount for one employee.

    Each line pairs an ``hr.employee_input_type`` with an ``amount``
    that salary rule Python code can read through the ``emp_inputs``
    local variable, independently of any single payslip.
    """

    _name = "hr.employee_input"

    _description = "Employee Input"

    employee_id = fields.Many2one(
        string="Payslip",
        comodel_name="hr.employee",
        required=True,
        ondelete="cascade",
    )
    input_type_id = fields.Many2one(
        string="Input Type",
        comodel_name="hr.employee_input_type",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        default=0.0,
    )

    @api.onchange("input_type_id")
    def _onchange_input_type_id(self):
        if self.input_type_id:
            self.amount = self.input_type_id.default_amount
