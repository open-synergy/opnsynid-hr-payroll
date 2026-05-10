# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrPayslipBatch(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends hr.payslip_batch with operating unit support.
    Adds mixin.single_operating_unit so payslip batch documents
    can be scoped to a specific operating unit.
    Overrides _prepare_payslip_data to propagate operating_unit_id
    to each generated payslip.
    """

    _name = "hr.payslip_batch"
    _inherit = [
        "hr.payslip_batch",
        "mixin.single_operating_unit",
    ]

    def _prepare_payslip_data(self, employee):
        res = super()._prepare_payslip_data(employee)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
