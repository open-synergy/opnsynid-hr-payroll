# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    batch_id = fields.Many2one(
        string="Payslip Batch",
        comodel_name="hr.payslip_batch",
        ondelete="cascade",
    )
