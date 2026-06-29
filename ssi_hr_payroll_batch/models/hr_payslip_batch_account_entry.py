# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models


class HrPayslipBatchAccountEntry(models.Model):
    _name = "hr.payslip_batch_account_entry"
    _description = "Payslip Batch Account Entry"
    _inherit = [
        "mixin.account_move_double_line",
    ]

    # -- mixin.account_move_double_line config --
    _move_id_field_name = "move_id"
    _currency_id_field_name = "company_currency_id"

    _debit_account_id_field_name = "debit_account_id"
    _credit_account_id_field_name = "credit_account_id"

    _debit_partner_id_field_name = "partner_id"
    _credit_partner_id_field_name = "partner_id"

    _debit_analytic_account_id_field_name = "analytic_account_id"
    _credit_analytic_account_id_field_name = "analytic_account_id"

    _debit_amount_currency_field_name = "amount"
    _credit_amount_currency_field_name = "amount"

    _debit_currency_id_field_name = "company_currency_id"
    _credit_currency_id_field_name = "company_currency_id"

    _debit_company_currency_id_field_name = "company_currency_id"
    _credit_company_currency_id_field_name = "company_currency_id"

    _debit_date_field_name = "date"
    _credit_date_field_name = "date"

    _debit_company_id_field_name = "company_id"
    _credit_company_id_field_name = "company_id"

    # -- fields --
    batch_id = fields.Many2one(
        string="Payslip Batch",
        comodel_name="hr.payslip_batch",
        required=True,
        ondelete="cascade",
        help="Payslip batch this aggregation entry belongs to.",
    )
    rule_id = fields.Many2one(
        string="Salary Rule",
        comodel_name="hr.salary_rule",
        required=True,
        ondelete="restrict",
        help="Salary rule that generated this aggregated amount.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        ondelete="restrict",
        help="Partner for this journal line (from contributor or employee home address). "
        "Empty when no contributor is set on the rule.",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
        ondelete="restrict",
        help="Account to debit for this aggregated salary rule.",
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
        ondelete="restrict",
        help="Account to credit for this aggregated salary rule.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="company_currency_id",
        help="Total aggregated amount for this (rule, partner) group.",
    )
    debit_move_line_id = fields.Many2one(
        string="Debit Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
        help="Debit move line created for this entry.",
    )
    credit_move_line_id = fields.Many2one(
        string="Credit Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
        help="Credit move line created for this entry.",
    )

    # -- related fields from batch --
    move_id = fields.Many2one(
        string="Journal Entry",
        comodel_name="account.move",
        related="batch_id.move_id",
        store=False,
        help="Journal entry of the parent batch.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        related="batch_id.analytic_account_id",
        store=False,
        help="Analytic account inherited from the batch.",
    )
    date = fields.Date(
        string="Date",
        related="batch_id.date",
        store=False,
        help="Accounting date inherited from the batch.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="batch_id.company_id",
        store=False,
        help="Company inherited from the batch.",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="batch_id.company_currency_id",
        store=False,
        help="Company currency inherited from the batch.",
    )

    def _get_standard_label(self, direction):
        self.ensure_one()
        return self.rule_id.name or False

    def _create_standard_ml(self):
        self.ensure_one()
        ML = self.env["account.move.line"].with_context(check_move_validity=False)
        debit_ml = self.env["account.move.line"]
        credit_ml = self.env["account.move.line"]
        if self.debit_account_id:
            debit_ml = ML.create(self._prepare_standard_ml("debit"))
        if self.credit_account_id:
            credit_ml = ML.create(self._prepare_standard_ml("credit"))
        return debit_ml, credit_ml

    def _reconcile_debit(self, candidate_ml):
        """Reconcile the debit move line against candidate reference lines."""
        self.ensure_one()
        if not self.debit_move_line_id:
            return
        acc = self.debit_move_line_id.account_id
        refs = candidate_ml.filtered(
            lambda l: l.account_id == acc
            and l.credit > 0.0
            and not l.reconciled
            and (not self.partner_id or l.partner_id == self.partner_id)
        )
        if refs:
            (refs + self.debit_move_line_id).reconcile()

    def _reconcile_credit(self, candidate_ml):
        """Reconcile the credit move line against candidate reference lines."""
        self.ensure_one()
        if not self.credit_move_line_id:
            return
        acc = self.credit_move_line_id.account_id
        refs = candidate_ml.filtered(
            lambda l: l.account_id == acc
            and l.debit > 0.0
            and not l.reconciled
            and (not self.partner_id or l.partner_id == self.partner_id)
        )
        if refs:
            (refs + self.credit_move_line_id).reconcile()

    def name_get(self):
        result = []
        for record in self:
            name = _("%s / %s") % (
                record.batch_id.display_name or str(record.batch_id.id),
                record.rule_id.name or str(record.rule_id.id),
            )
            result.append((record.id, name))
        return result
