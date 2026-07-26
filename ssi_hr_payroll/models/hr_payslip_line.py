# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class HrPayslipLine(models.Model):
    """
    Represents one computed salary rule result on a payslip.

    Stores the amount produced by evaluating a ``hr.salary_rule`` for
    a given ``hr.payslip``, together with the ``account.move.line``
    records created and reconciled for it once the payslip is done.
    """

    _name = "hr.payslip_line"

    _description = "Payslip Input"

    payslip_id = fields.Many2one(
        string="Payslip",
        comodel_name="hr.payslip",
        required=True,
        ondelete="cascade",
    )
    rule_id = fields.Many2one(
        string="Salary Rule",
        comodel_name="hr.salary_rule",
        required=True,
        ondelete="restrict",
    )
    category_id = fields.Many2one(
        string="Salary Rule Category", related="rule_id.category_id"
    )
    move_line_debit_id = fields.Many2one(
        string="Move Line Debit",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    move_line_credit_id = fields.Many2one(
        string="Move Line Credit",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    rate = fields.Float(
        string="Rate (%)",
        default=100.0,
    )
    amount = fields.Float(
        string="Amount",
    )
    quantity = fields.Float(
        string="Quantity",
    )

    @api.depends(
        "quantity",
        "amount",
        "rate",
    )
    def _compute_total(self):
        """Compute ``total`` as ``quantity * amount * rate / 100``."""
        for document in self:
            quantity = float(document.quantity)
            amount = document.amount
            rate = document.rate
            document.total = (quantity * amount) * (rate / 100)

    total = fields.Float(
        string="Total",
        compute="_compute_total",
    )

    def _get_partner_id(self):
        """Resolve the partner the accounting entry is booked against.

        Uses the rule's ``contribution_id.partner_id`` when the
        salary rule is linked to a ``hr.salary_contribution`` with a
        partner set; otherwise falls back to the payslip employee's
        home address partner. Returns ``False`` when no contribution
        is configured on the rule.

        :return: ``res.partner`` id, or ``False``
        """
        self.ensure_one()
        partner_id = False
        contribution = self.rule_id.contribution_id
        if contribution and contribution.partner_id:
            partner_id = contribution.partner_id.id
        elif contribution and not contribution.partner_id:
            partner_id = self.payslip_id.employee_id.address_home_id.id
        return partner_id

    def _get_account_by_product_usage(self, usage):
        """Resolve the account for ``usage`` on the rule's product.

        :param usage: a ``product.usage_type`` record
        :return: ``account.account`` id resolved through the rule's
            ``product_id``, or ``False`` when ``usage`` or the
            product is not set
        """
        self.ensure_one()
        if not usage or not self.rule_id.product_id:
            return False
        return self.rule_id.product_id._get_product_account(usage.code)

    def _get_debit_account(self):
        """Resolve the debit account used for this line's entry.

        Falls back to the rule's ``debit_account_id`` when the
        payslip has no ``debit_usage_id``, or when the product usage
        lookup does not resolve an account.

        :return: ``account.account`` record, possibly empty
        """
        self.ensure_one()
        debit_account = self.rule_id.debit_account_id
        if not debit_account:
            return debit_account
        if self.payslip_id.debit_usage_id:
            usage_account = self._get_account_by_product_usage(
                self.payslip_id.debit_usage_id
            )
            if usage_account:
                return usage_account
        return debit_account

    def _get_credit_account(self):
        """Resolve the credit account used for this line's entry.

        Falls back to the rule's ``credit_account_id`` when the
        payslip has no ``credit_usage_id``, or when the product usage
        lookup does not resolve an account.

        :return: ``account.account`` record, possibly empty
        """
        self.ensure_one()
        credit_account = self.rule_id.credit_account_id
        if not credit_account:
            return credit_account
        if self.payslip_id.credit_usage_id:
            usage_account = self._get_account_by_product_usage(
                self.payslip_id.credit_usage_id
            )
            if usage_account:
                return usage_account
        return credit_account

    def _prepare_aml_debit_data(self, move):
        """Build the debit ``account.move.line`` values for this line.

        Extension point: override to add analytic or operating unit
        fields without touching ``create_move_line``.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        payslip = self.payslip_id
        debit_account_id = self._get_debit_account().id
        amount = self.amount
        name = _("%s for %s") % (self.rule_id.name, payslip.name)

        data = {
            "move_id": move.id,
            "name": name,
            "partner_id": self._get_partner_id(),
            "account_id": debit_account_id,
            "journal_id": payslip.journal_id.id,
            "debit": amount > 0.0 and amount or 0.0,
            "credit": amount < 0.0 and -amount or 0.0,
        }
        if payslip.analytic_account_id:
            data["analytic_account_id"] = payslip.analytic_account_id.id
        return data

    def _prepare_aml_credit_data(self, move):
        """Build the credit ``account.move.line`` values for this line.

        Extension point: override to add analytic or operating unit
        fields without touching ``create_move_line``.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        payslip = self.payslip_id
        credit_account_id = self._get_credit_account().id
        amount = self.amount
        name = _("%s for %s") % (self.rule_id.name, payslip.name)

        data = {
            "move_id": move.id,
            "name": name,
            "partner_id": self._get_partner_id(),
            "account_id": credit_account_id,
            "journal_id": payslip.journal_id.id,
            "debit": amount < 0.0 and -amount or 0.0,
            "credit": amount > 0.0 and amount or 0.0,
        }
        if payslip.analytic_account_id:
            data["analytic_account_id"] = payslip.analytic_account_id.id
        return data

    def create_move_line(self, move):
        """Create the debit and credit journal items for these lines.

        For each line with a non-zero ``amount``, creates an
        ``account.move.line`` on ``move`` for the resolved debit
        and/or credit account and stores it back on
        ``move_line_debit_id`` / ``move_line_credit_id``. Runs under
        ``sudo()`` and skips move validity checks while creating the
        items.

        :param move: the ``account.move`` to attach the journal
            items to
        :return: tuple ``(debit_sum, credit_sum)`` of the net debit
            and credit amounts created
        """
        obj_account_move_line = self.env["account.move.line"].with_context(
            check_move_validity=False
        )
        debit_sum = 0.0
        credit_sum = 0.0

        for document in self.filtered(lambda l: l.amount).sudo():
            if document._get_debit_account():
                debit_data = document._prepare_aml_debit_data(move)
                debit_sum += debit_data["debit"] - debit_data["credit"]
                move_line = obj_account_move_line.create(debit_data)
                if move_line.debit > 0:
                    document.move_line_debit_id = move_line.id
                elif move_line.credit > 0:
                    document.move_line_credit_id = move_line.id
            if document._get_credit_account():
                credit_data = document._prepare_aml_credit_data(move)
                credit_sum += credit_data["credit"] - credit_data["debit"]
                move_line = obj_account_move_line.create(credit_data)
                if move_line.debit > 0:
                    document.move_line_debit_id = move_line.id
                elif move_line.credit > 0:
                    document.move_line_credit_id = move_line.id

        return debit_sum, credit_sum

    def _reconcile_debit(self):
        """Reconcile this line's debit item against allowance refs.

        Searches the payslip's ``allowance_ref_move_line_ids`` on the
        same account for a matching credit line and reconciles it
        together with ``move_line_debit_id``.
        """
        self.ensure_one()

        ML = self.env["account.move.line"]

        criteria = [
            ("account_id", "=", self.move_line_debit_id.account_id.id),
            ("credit", ">", 0.0),
            ("id", "in", self.payslip_id.allowance_ref_move_line_ids.ids),
        ]

        move_lines = ML.search(criteria)
        (move_lines + self.move_line_debit_id).reconcile()

    def _reconcile_credit(self):
        """Reconcile this line's credit item against deduction refs.

        Searches the payslip's ``deduction_ref_move_line_ids`` on the
        same account for a matching debit line and reconciles it
        together with ``move_line_credit_id``.
        """
        self.ensure_one()
        ML = self.env["account.move.line"]

        criteria = [
            ("account_id.id", "=", self.move_line_credit_id.account_id.id),
            ("debit", ">", 0.0),
            ("id", "in", self.payslip_id.deduction_ref_move_line_ids.ids),
        ]

        move_lines = ML.search(criteria)
        (move_lines + self.move_line_credit_id).reconcile()

    def _unreconcile_debit(self):
        """Undo the reconciliation of ``move_line_debit_id``, if any."""
        self.move_line_debit_id.remove_move_reconcile()

    def _unreconcile_credit(self):
        """Undo the reconciliation of ``move_line_credit_id``, if any."""
        self.move_line_credit_id.remove_move_reconcile()
