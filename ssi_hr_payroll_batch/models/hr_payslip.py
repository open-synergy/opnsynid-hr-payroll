# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrPayslip(models.Model):
    """
    Links a payslip to the ``hr.payslip_batch`` that generated it.

    When ``batch_id`` is set, this payslip's individual journaling is
    skipped in favour of the batch-level entry (see
    ``_need_accounting_entry``), and its workflow actions are locked
    so it can only be driven through the batch (see
    ``_check_batch_lock``), keeping every payslip of a batch in sync
    with the batch's own state.
    """

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
        """Raise if called directly on a batched payslip.

        Applies only when there is no batch context, i.e. the payslip
        belongs to a batch but was not driven through it.

        :param action_name: label of the action being attempted, used
            in the raised error message
        :raises UserError: if ``batch_id`` is set and the call is not
            flagged with the ``from_batch`` context key
        """
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
        """Confirm the payslip.

        Overridden only to enforce ``_check_batch_lock`` before
        delegating to the inherited transition.
        """
        for record in self:
            record._check_batch_lock("Confirm")
        return super().action_confirm()

    def action_approve_approval(self):
        """Approve the payslip.

        Overridden only to enforce ``_check_batch_lock`` before
        delegating to the inherited transition.
        """
        for record in self:
            record._check_batch_lock("Approve")
        return super().action_approve_approval()

    def action_done(self):
        """Mark the payslip as done.

        Overridden only to enforce ``_check_batch_lock`` before
        delegating to the inherited transition.
        """
        for record in self:
            record._check_batch_lock("Done")
        return super().action_done()

    def action_cancel(self, cancel_reason=False):
        """Cancel the payslip.

        Overridden only to enforce ``_check_batch_lock`` before
        delegating to the inherited transition.

        :param cancel_reason: ``ssi_transaction_cancel_mixin`` cancel
            reason record
        """
        for record in self:
            record._check_batch_lock("Cancel")
        return super().action_cancel(cancel_reason)

    def action_restart(self):
        """Restart the payslip.

        Overridden only to enforce ``_check_batch_lock`` before
        delegating to the inherited transition.
        """
        for record in self:
            record._check_batch_lock("Restart")
        return super().action_restart()
