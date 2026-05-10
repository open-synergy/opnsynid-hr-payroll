# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):  # pylint: disable=too-few-public-methods
    """
    Extends hr.payslip with a constraint to ensure that
    a payslip's operating_unit_id matches its batch's operating_unit_id.
    """

    _name = "hr.payslip"
    _inherit = "hr.payslip"

    @api.constrains("batch_id", "operating_unit_id")
    def _check_batch_operating_unit(self):
        for document in self.sudo():
            if not document._check_payslip_batch_operating_unit_condition():
                # pylint: disable=consider-using-f-string
                error_message = """
Context: Check payslip operating unit consistency with batch
Database ID: %s
Problem: Payslip operating unit (%s) does not match batch operating unit (%s)
Solution: Ensure the payslip operating unit is the same as the batch operating unit
""" % (
                    document.id,
                    document.operating_unit_id.name,
                    document.batch_id.operating_unit_id.name,
                )
                # pylint: enable=consider-using-f-string
                raise ValidationError(_(error_message))

    def _check_payslip_batch_operating_unit_condition(self):
        self.ensure_one()
        if not self.batch_id:
            return True
        return self.operating_unit_id == self.batch_id.operating_unit_id
