# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrEmployeeInputType(models.Model):  # pylint: disable=too-few-public-methods
    """
    Defines a reusable category of recurring per-employee payroll input.

    Each type carries a ``default_amount`` that seeds new
    ``hr.employee_input`` lines, and its ``code`` is looked up by
    salary rule Python code through the ``emp_inputs`` local variable.
    """

    _name = "hr.employee_input_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Employee Input Type"

    default_amount = fields.Float(
        string="Default Amount",
        default=0.0,
    )
