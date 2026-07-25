# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrPayslipBatch(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends hr.payslip_batch with operating unit support.
    Adds mixin.single_operating_unit so payslip batch documents
    can be scoped to a specific operating unit.
    Overrides _compute_employee_ids to filter allowed employees by the batch OU.
    Overrides _prepare_payslip_data to propagate operating_unit_id
    to each generated payslip.
    Overrides _prepare_standard_move to propagate operating_unit_id
    to the batch-level journal entry.
    """

    _name = "hr.payslip_batch"
    _inherit = [
        "hr.payslip_batch",
        "mixin.single_operating_unit",
    ]

    @api.depends(
        "operating_unit_id",
    )
    def _compute_employee_ids(self):
        super()._compute_employee_ids()
        for document in self:
            if document.operating_unit_id:
                employee_ids = document.allowed_employee_ids.filtered(
                    lambda employee, ou=document.operating_unit_id: employee.operating_unit_id
                    == ou
                )
                document.allowed_employee_ids = [(6, 0, employee_ids.ids)]

    def _prepare_payslip_data(self, employee):
        res = super()._prepare_payslip_data(employee)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _prepare_standard_move(self):
        res = super()._prepare_standard_move()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
