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
        """Restrict ``allowed_employee_ids`` to the batch's OU.

        Calls ``super()`` first to compute the base candidate list, then
        filters it down to employees whose ``operating_unit_id`` matches
        the batch's ``operating_unit_id`` when one is set. Batches without
        an ``operating_unit_id`` keep the unfiltered list from ``super()``.
        """
        super()._compute_employee_ids()
        for document in self:
            if document.operating_unit_id:
                employee_ids = document.allowed_employee_ids.filtered(
                    lambda employee, ou=document.operating_unit_id: employee.operating_unit_id
                    == ou
                )
                document.allowed_employee_ids = [(6, 0, employee_ids.ids)]

    def _prepare_payslip_data(self, employee):
        """Build ``hr.payslip`` values for ``employee``, adding the OU.

        Extension point: adds ``operating_unit_id`` from the batch to the
        values dict returned by ``super()`` so each generated payslip
        inherits the batch's operating unit.

        :param employee: ``hr.employee`` record the payslip is created for
        :return: dict of ``hr.payslip`` values
        """
        res = super()._prepare_payslip_data(employee)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _prepare_standard_move(self):
        """Build ``account.move`` values, propagating the batch OU.

        Extension point: adds ``operating_unit_id`` from the batch to the
        values dict returned by ``super()`` so the batch-level journal
        entry carries the same operating unit as the batch.

        :return: dict of ``account.move`` values
        """
        res = super()._prepare_standard_move()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
