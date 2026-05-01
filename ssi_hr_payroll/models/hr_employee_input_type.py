# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrEmployeeInputType(models.Model):  # pylint: disable=too-few-public-methods
    _name = "hr.employee_input_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Employee Input Type"

    default_amount = fields.Float(
        string="Default Amount",
        default=0.0,
    )
