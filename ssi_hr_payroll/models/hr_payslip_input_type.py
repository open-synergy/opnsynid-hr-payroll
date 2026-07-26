# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


# pylint: disable=duplicate-code
class HrPayslipInputType(models.Model):  # pylint: disable=too-few-public-methods
    """
    Defines a reusable category of per-payslip input.

    Each type carries a ``default_amount`` that seeds new
    ``hr.payslip_input`` lines, and its ``code`` is looked up by
    salary rule Python code through the ``inputs`` local variable.
    """

    _name = "hr.payslip_input_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Payslip Input Type"

    default_amount = fields.Float(
        string="Default Amount",
        default=0.0,
    )
