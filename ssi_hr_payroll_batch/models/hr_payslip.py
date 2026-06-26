# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    batch_id = fields.Many2one(
        string="Payslip Batch",
        comodel_name="hr.payslip_batch",
        ondelete="cascade",
    )

    def _need_accounting_entry(self):
        """Skip payslip-level journaling when the batch handles it."""
        self.ensure_one()
        if self.batch_id and self.batch_id.accounting_method == "batch":
            return False
        return super()._need_accounting_entry()

    def _check_batch_lock(self, action_name):
        """Raise if called directly on a batched payslip without batch context."""
        self.ensure_one()
        if self.batch_id and not self.env.context.get("from_batch"):
            raise UserError(
                _(
                    """
Context: Payslip workflow action '%s'
Database ID: %s
Problem: This payslip belongs to a batch and cannot be processed individually
Solution: Use the payslip batch workflow to drive payslip state changes
                """
                )
                % (action_name, self.id)
            )

    def action_confirm(self):
        for record in self:
            record._check_batch_lock("Confirm")
        return super().action_confirm()

    def action_approve_approval(self):
        for record in self:
            record._check_batch_lock("Approve")
        return super().action_approve_approval()

    def action_done(self):
        for record in self:
            record._check_batch_lock("Done")
        return super().action_done()

    def action_cancel(self, cancel_reason=False):
        for record in self:
            record._check_batch_lock("Cancel")
        return super().action_cancel(cancel_reason)

    def action_restart(self):
        for record in self:
            record._check_batch_lock("Restart")
        return super().action_restart()
