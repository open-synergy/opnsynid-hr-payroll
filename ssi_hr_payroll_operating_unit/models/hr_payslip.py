# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrPayslip(models.Model):
    """
    Extends hr.payslip with operating unit support.
    Adds mixin.single_operating_unit so payslip documents
    can be scoped to a specific operating unit.
    Overrides _compute_allowed_employee_ids to filter allowed employees
    by the payslip OU.
    Overrides _prepare_account_move_data to propagate operating_unit_id
    to the generated accounting entry.
    """

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "mixin.single_operating_unit",
    ]

    @api.depends(
        "operating_unit_id",
    )
    def _compute_allowed_employee_ids(self):
        """Restrict ``allowed_employee_ids`` to the payslip's OU.

        Calls ``super()`` first to compute the base candidate list, then
        filters it down to employees whose ``operating_unit_id`` matches
        the payslip's ``operating_unit_id`` when one is set. Payslips
        without an ``operating_unit_id`` keep the unfiltered list from
        ``super()``.
        """
        super()._compute_allowed_employee_ids()
        for record in self:
            if record.operating_unit_id:
                employee_ids = record.allowed_employee_ids.filtered(
                    lambda employee, ou=record.operating_unit_id: employee.operating_unit_id
                    == ou
                )
                record.allowed_employee_ids = [(6, 0, employee_ids.ids)]

    def _prepare_account_move_data(self):
        """Add ``operating_unit_id`` to the ``account.move`` values.

        Overridden so the accounting entry generated for this payslip
        is scoped to the same operating unit as the payslip itself.

        :return: dict of ``account.move`` values
        """
        res = super()._prepare_account_move_data()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
