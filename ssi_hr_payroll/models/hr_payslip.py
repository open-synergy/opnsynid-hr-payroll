# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from pytz import timezone

import odoo
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

from odoo.addons.ssi_decorator import ssi_decorator


class BrowsableObject(object):
    """Expose a plain dict as attribute lookups for Python code.

    Base class for the objects injected into the localdict passed to
    ``safe_eval`` when evaluating a salary rule's ``condition_python``
    / ``amount_python``; missing keys resolve to ``0.0`` instead of
    raising ``AttributeError``.
    """

    def __init__(self, employee_id, vals_dict, env):
        """Store the employee id, backing dict and environment."""
        self.employee_id = employee_id
        self.dict = vals_dict
        self.env = env

    def __getattr__(self, attr):
        """Return ``vals_dict[attr]`` if present, else ``0.0``."""
        return attr in self.dict and self.dict.__getitem__(attr) or 0.0


class Payslips(BrowsableObject):
    """a class that will be used into the python code, mainly for
    usability purposes"""

    def sum(self, code, from_date, to_date=None):
        """Sum a salary rule's ``total`` across posted payslips.

        Reads directly from ``hr_payslip``/``hr_payslip_line`` for
        payslips of this employee in state ``done`` whose
        ``date_from``/``date_to`` fall within the given range,
        negating the amount when the payslip is a credit note.

        :param code: ``hr.salary_rule`` code to sum
        :param from_date: lower bound of ``date_from``
        :param to_date: upper bound of ``date_to``; defaults to today
        :return: summed ``total``, or ``0.0`` if nothing matches
        """
        if to_date is None:
            to_date = fields.Date.today()
        self.env.cr.execute(
            """SELECT sum(case when hp.credit_note = False then
            (pl.total) else (-pl.total) end)
                    FROM hr_payslip as hp, hr_payslip_line as pl
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND
                     hp.id = pl.slip_id AND pl.code = %s""",
            (self.employee_id, from_date, to_date, code),
        )
        res = self.env.cr.fetchone()
        return res and res[0] or 0.0


class InputLine(BrowsableObject):
    """a class that will be used into the python code, mainly for
    usability purposes"""

    def sum(self, code, from_date, to_date=None):
        """Sum a payslip input's ``amount`` across posted payslips.

        Reads directly from ``hr_payslip``/``hr_payslip_input`` for
        payslips of this employee in state ``done`` whose
        ``date_from``/``date_to`` fall within the given range.

        :param code: ``hr.payslip_input_type`` code to sum
        :param from_date: lower bound of ``date_from``
        :param to_date: upper bound of ``date_to``; defaults to today
        :return: summed ``amount``, or ``0.0`` if nothing matches
        """
        if to_date is None:
            to_date = fields.Date.today()
        self.env.cr.execute(
            """
            SELECT sum(amount) as sum
            FROM hr_payslip as hp, hr_payslip_input as pi
            WHERE hp.employee_id = %s AND hp.state = 'done'
            AND hp.date_from >= %s AND hp.date_to <= %s
            AND hp.id = pi.payslip_id AND pi.code = %s""",
            (self.employee_id, from_date, to_date, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class EmployeeInputLine(BrowsableObject):
    """Expose an employee's recurring input amounts by code.

    Backs the ``emp_inputs`` local variable made available to salary
    rule Python code.
    """

    def sum(self, code):
        """Sum an employee input's ``amount`` for a given code.

        Reads directly from ``hr_employee_input`` /
        ``hr_employee_input_type`` for this employee, independently
        of any single payslip.

        :param code: ``hr.employee_input_type`` code to sum
        :return: summed ``amount``, or ``0.0`` if nothing matches
        """
        self.env.cr.execute(
            """
            SELECT sum(b.amount) as sum
            FROM hr_employee as a
            JOIN hr_employee_input as b ON a.id=b.employee_id
            JOIN hr_employee_input_type as c ON b.input_type_id=c.id
            WHERE a.id = %s AND c.code = %s""",
            (self.employee_id, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class HrPayslip(models.Model):
    """
    Represents a single employee payslip and drives its computation.

    Combines an employee's ``hr.salary_structure`` with the payslip's
    input lines to evaluate every applicable ``hr.salary_rule`` and
    produce ``hr.payslip_line`` results, then books the resulting
    debit/credit ``account.move.line`` entries once the payslip is
    confirmed and approved. Goes through the mixin-provided
    draft -> confirm -> done/cancel/reject workflow.
    """

    _name = "hr.payslip"
    _description = "Employee Payslip"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.employee_document",
        "mixin.date_duration",
        "mixin.many2one_configurator",
    ]
    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Sequence attribute
    _create_sequence_state = "done"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.payslip_type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    structure_id = fields.Many2one(
        string="Salary Structure",
        comodel_name="hr.salary_structure",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    rule_ids = fields.Many2many(
        string="All Salary Rules",
        comodel_name="hr.salary_rule",
        compute="_compute_rule_ids",
        store=False,
    )
    line_ids = fields.One2many(
        string="Payslip Lines",
        comodel_name="hr.payslip_line",
        inverse_name="payslip_id",
        readonly=True,
        copy=False,
    )
    input_line_ids = fields.One2many(
        string="Input Types",
        comodel_name="hr.payslip_input",
        inverse_name="payslip_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
    )
    allowed_allowance_move_line_ids = fields.Many2many(
        string="Allowed Allowance Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_allowance_move_line_ids",
        store=False,
    )

    allowance_ref_move_line_ids = fields.Many2many(
        string="Allowance Ref Move Lines",
        comodel_name="account.move.line",
        relation="rel_payslip_2_allowance_ml",
        column1="payslip_id",
        column2="move_line_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_deduction_move_line_ids = fields.Many2many(
        string="Allowed Deduction Ref Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_deduction_move_line_ids",
        store=False,
    )
    deduction_ref_move_line_ids = fields.Many2many(
        string="Deduction Ref Move Lines",
        comodel_name="account.move.line",
        relation="rel_payslip_2_deduction_ml",
        column1="payslip_id",
        column2="move_line_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Accounting journal used for this payslip entry.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Analytic account used for all journal items of this payslip.",
    )
    debit_usage_id = fields.Many2one(
        string="Debit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Product usage type used to resolve the debit account " "of this payslip.",
    )
    credit_usage_id = fields.Many2one(
        string="Credit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Product usage type used to resolve the credit account "
        "of this payslip.",
    )
    allowed_analytic_account_ids = fields.Many2many(
        string="Allowed Analytic Accounts",
        comodel_name="account.analytic.account",
        compute="_compute_allowed_analytic_account_ids",
        store=False,
        compute_sudo=True,
        help="Analytic accounts allowed on 'Analytic Account' as configured "
        "on the payslip type's M2O configurator.",
    )
    allowed_debit_usage_ids = fields.Many2many(
        string="Allowed Debit Usages",
        comodel_name="product.usage_type",
        compute="_compute_allowed_debit_usage_ids",
        store=False,
        compute_sudo=True,
        help="Product usage types allowed on 'Debit Usage' as configured on "
        "the payslip type's M2O configurator.",
    )
    allowed_credit_usage_ids = fields.Many2many(
        string="Allowed Credit Usages",
        comodel_name="product.usage_type",
        compute="_compute_allowed_credit_usage_ids",
        store=False,
        compute_sudo=True,
        help="Product usage types allowed on 'Credit Usage' as configured on "
        "the payslip type's M2O configurator.",
    )
    allowed_employee_ids = fields.Many2many(
        string="Allowed Employees",
        comodel_name="hr.employee",
        compute="_compute_allowed_employee_ids",
        store=False,
        compute_sudo=True,
        help="Employees allowed on 'Employee' as configured on the payslip "
        "type's M2O configurator.",
    )
    debit_account_2b_reconciled_ids = fields.Many2many(
        string="Debit Accounts To Be Reconciled",
        comodel_name="account.account",
        compute="_compute_debit_account_2b_reconciled_ids",
        store=False,
    )
    credit_account_2b_reconciled_ids = fields.Many2many(
        string="Credit Accounts To Be Reconciled",
        comodel_name="account.account",
        compute="_compute_credit_account_2b_reconciled_ids",
        store=False,
    )
    move_id = fields.Many2one(
        string="# Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
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
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.depends(
        "structure_id",
    )
    def _compute_rule_ids(self):
        """Compute ``rule_ids`` from the structure's rule hierarchy.

        Expands ``structure_id`` and all of its ancestors through
        ``hr.salary_structure._get_parent_structure`` /
        ``get_all_rules``, sorted by rule ``sequence``.
        """
        for record in self:
            result = []
            if record.structure_id:
                structures = record.structure_id._get_parent_structure()
                rule_list = structures.get_all_rules()
                result = [id for id, sequence in sorted(rule_list, key=lambda x: x[1])]
            record.rule_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        """Compute the analytic accounts selectable on this payslip.

        Delegates to ``_m2o_configurator_get_filter`` using
        ``type_id``'s analytic account selection method (manual/
        domain/Python code). Without a ``type_id`` yet, falls back to
        every ``account.analytic.account`` so the field stays usable
        while the form is being filled in.
        """
        # No type_id yet (e.g. the Employee field is filled in before Type on
        # a new record): behave like the type's own "no restriction" default
        # (selection_method="domain", domain="[]") instead of blocking every
        # record, so the field stays usable while the form is being filled in.
        AnalyticAccount = self.env["account.analytic.account"]
        for record in self:
            result = AnalyticAccount.search([])
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.analytic.account",
                    method_selection=record.type_id.analytic_account_selection_method,
                    manual_recordset=record.type_id.analytic_account_ids,
                    domain=record.type_id.analytic_account_domain,
                    python_code=record.type_id.analytic_account_python_code,
                )
            record.allowed_analytic_account_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_debit_usage_ids(self):
        """Compute the debit product usages selectable on this payslip.

        Delegates to ``_m2o_configurator_get_filter`` using
        ``type_id``'s debit usage selection method (manual/domain/
        Python code). Without a ``type_id`` yet, falls back to every
        ``product.usage_type`` so the field stays usable while the
        form is being filled in.
        """
        # See _compute_allowed_analytic_account_ids for why the no-type_id
        # default is an unrestricted search rather than an empty result.
        ProductUsage = self.env["product.usage_type"]
        for record in self:
            result = ProductUsage.search([])
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.usage_type",
                    method_selection=record.type_id.debit_usage_selection_method,
                    manual_recordset=record.type_id.debit_usage_ids,
                    domain=record.type_id.debit_usage_domain,
                    python_code=record.type_id.debit_usage_python_code,
                )
            record.allowed_debit_usage_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_credit_usage_ids(self):
        """Compute the credit product usages selectable on this payslip.

        Delegates to ``_m2o_configurator_get_filter`` using
        ``type_id``'s credit usage selection method (manual/domain/
        Python code). Without a ``type_id`` yet, falls back to every
        ``product.usage_type`` so the field stays usable while the
        form is being filled in.
        """
        # See _compute_allowed_analytic_account_ids for why the no-type_id
        # default is an unrestricted search rather than an empty result.
        ProductUsage = self.env["product.usage_type"]
        for record in self:
            result = ProductUsage.search([])
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.usage_type",
                    method_selection=record.type_id.credit_usage_selection_method,
                    manual_recordset=record.type_id.credit_usage_ids,
                    domain=record.type_id.credit_usage_domain,
                    python_code=record.type_id.credit_usage_python_code,
                )
            record.allowed_credit_usage_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_employee_ids(self):
        """Compute the employees selectable on this payslip.

        Delegates to ``_m2o_configurator_get_filter`` using
        ``type_id``'s employee selection method (manual/domain/
        Python code). Without a ``type_id`` yet, falls back to every
        ``hr.employee`` so the field stays usable while the form is
        being filled in.
        """
        # See _compute_allowed_analytic_account_ids for why the no-type_id
        # default is an unrestricted search rather than an empty result.
        Employee = self.env["hr.employee"]
        for record in self:
            result = Employee.search([])
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="hr.employee",
                    method_selection=record.type_id.employee_selection_method,
                    manual_recordset=record.type_id.employee_ids,
                    domain=record.type_id.employee_domain,
                    python_code=record.type_id.employee_python_code,
                )
            record.allowed_employee_ids = result

    @api.depends(
        "rule_ids",
    )
    def _compute_debit_account_2b_reconciled_ids(self):
        """Compute debit accounts eligible for allowance reconciliation.

        Collects ``reconcile_debit_account_id`` from every rule in
        ``rule_ids`` that has ``reconcile_debit`` enabled; used by
        ``_compute_allowed_allowance_move_line_ids``.
        """
        SalaryRule = self.env["hr.salary_rule"]
        for record in self:
            result = []
            criteria = [
                ("id", "in", record.rule_ids.ids),
                ("reconcile_debit_account_id", "!=", False),
                ("reconcile_debit", "=", True),
            ]
            for rule in SalaryRule.search(criteria):
                result.append(rule.reconcile_debit_account_id.id)
            record.debit_account_2b_reconciled_ids = result

    @api.depends(
        "rule_ids",
    )
    def _compute_credit_account_2b_reconciled_ids(self):
        """Compute credit accounts eligible for deduction reconciliation.

        Collects ``reconcile_credit_account_id`` from every rule in
        ``rule_ids`` that has ``reconcile_credit`` enabled; used by
        ``_compute_allowed_deduction_move_line_ids``.
        """
        SalaryRule = self.env["hr.salary_rule"]
        for record in self:
            result = []
            criteria = [
                ("id", "in", record.rule_ids.ids),
                ("reconcile_credit_account_id", "!=", False),
                ("reconcile_credit", "=", True),
            ]
            for rule in SalaryRule.search(criteria):
                result.append(rule.reconcile_credit_account_id.id)
            record.credit_account_2b_reconciled_ids = result

    @api.depends(
        "employee_id",
        "structure_id",
    )
    def _compute_allowed_deduction_move_line_ids(self):
        """Compute move lines eligible as deduction reference lines.

        Searches unreconciled debit ``account.move.line`` records for
        the employee's home address partner on
        ``credit_account_2b_reconciled_ids``.
        """
        ML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.employee_id and record.structure_id:
                criteria = [
                    ("partner_id", "=", record.employee_id.address_home_id.id),
                    ("account_id", "in", record.credit_account_2b_reconciled_ids.ids),
                    ("debit", ">", 0.0),
                    ("reconciled", "=", False),
                ]
                result = ML.search(criteria).ids
            record.allowed_deduction_move_line_ids = result

    @api.depends(
        "employee_id",
        "structure_id",
    )
    def _compute_allowed_allowance_move_line_ids(self):
        """Compute move lines eligible as allowance reference lines.

        Searches unreconciled credit ``account.move.line`` records
        for the employee's home address partner on
        ``debit_account_2b_reconciled_ids``.
        """
        ML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.employee_id and record.structure_id:
                criteria = [
                    ("partner_id", "=", record.employee_id.address_home_id.id),
                    ("account_id", "in", record.debit_account_2b_reconciled_ids.ids),
                    ("credit", ">", 0.0),
                    ("reconciled", "=", False),
                ]
                result = ML.search(criteria).ids
            record.allowed_allowance_move_line_ids = result

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_debit_usage_id(self):
        self.debit_usage_id = False
        if self.type_id:
            self.debit_usage_id = self.type_id.debit_usage_id

    @api.onchange(
        "type_id",
    )
    def onchange_credit_usage_id(self):
        self.credit_usage_id = False
        if self.type_id:
            self.credit_usage_id = self.type_id.credit_usage_id

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False
        if self.type_id:
            self.analytic_account_id = self.type_id.analytic_account_id

    @api.onchange(
        "structure_id",
    )
    def onchange_input_line_ids(self):
        """Rebuild ``input_line_ids`` from the selected structure.

        Clears the current input lines, then re-creates one new
        (unsaved) ``hr.payslip_input`` command per input type
        resolved from ``_get_input_line_ids`` for the current
        ``structure_id``.
        """
        res = []
        self.input_line_ids = False
        if self.structure_id:
            input_line_ids = self._get_input_line_ids()
            if input_line_ids:
                for input_line in input_line_ids:
                    res.append((0, 0, input_line))
        self.input_line_ids = res

    @api.onchange(
        "employee_id",
    )
    def onchange_structure_id(self):
        self.structure_id = False
        if self.employee_id:
            self.structure_id = self.employee_id.salary_structure_id

    def action_recompute_allowance_ref(self):
        """Refresh ``allowance_ref_move_line_ids`` for these payslips.

        Runs under ``sudo()`` and delegates to
        ``_recompute_allowance_ref`` for each record.
        """
        for record in self.sudo():
            record._recompute_allowance_ref()

    def action_recompute_deduction_ref(self):
        """Refresh ``deduction_ref_move_line_ids`` for these payslips.

        Runs under ``sudo()`` and delegates to
        ``_recompute_deduction_ref`` for each record.
        """
        for record in self.sudo():
            record._recompute_deduction_ref()

    def action_reload_input_lines(self):
        """Reload ``input_line_ids`` for these payslips.

        Runs under ``sudo()`` and delegates to
        ``_reload_input_lines`` for each record.
        """
        for record in self.sudo():
            record._reload_input_lines()

    def action_compute_payslip(self):
        """Recompute reference lines and salary rule results.

        Runs under ``sudo()`` and, for each payslip, refreshes the
        allowance and deduction reference lines then re-evaluates
        the salary rules through ``_compute_payslip``.
        """
        for document in self.sudo():
            document._recompute_allowance_ref()
            document._recompute_deduction_ref()
            document._compute_payslip()

    @ssi_decorator.post_cancel_action()
    def _10_cancel_accounting_entry(self):
        """Undo the accounting entry created for this payslip.

        Runs after the payslip is cancelled. Cancels and deletes
        ``move_id`` (posting it to cancelled first if needed), clears
        ``move_line_debit_id`` / ``move_line_credit_id`` on the
        payslip and its lines, and unreconciles every line whose
        rule has ``reconcile_debit`` / ``reconcile_credit`` enabled.
        Does nothing when no ``move_id`` exists.
        """
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]

        if not self.move_id:
            return True

        move = self.move_id

        if self.move_id.state == "posted":
            self.move_id.button_cancel()

        self.write(
            {
                "move_line_debit_id": False,
                "move_line_credit_id": False,
                "move_id": False,
            }
        )

        debit_criteria = [
            ("payslip_id", "=", self.id),
            ("move_line_debit_id", "!=", False),
            ("rule_id.reconcile_debit", "=", True),
        ]
        for line in PayslipLine.search(debit_criteria):
            line._unreconcile_debit()

        credit_criteria = [
            ("payslip_id", "=", self.id),
            ("move_line_credit_id", "!=", False),
            ("rule_id.reconcile_credit", "=", True),
        ]
        for line in PayslipLine.search(credit_criteria):
            line._unreconcile_credit()

        for line in self.line_ids:
            line.write(
                {
                    "move_line_debit_id": False,
                    "move_line_credit_id": False,
                }
            )
        move.with_context(force_delete=True).unlink()

    def _need_accounting_entry(self):
        """Hook: return False to skip payslip-level journaling."""
        self.ensure_one()
        return True

    @ssi_decorator.post_done_action()
    def _10_create_accounting_entry(self):
        """Create the accounting entry for this payslip.

        Runs after the payslip is set to done, unless
        ``_need_accounting_entry`` returns ``False``. Creates
        ``move_id`` from ``_prepare_account_move_data``, then the
        debit/credit journal items for every ``line_ids`` through
        ``create_move_line``, adds a balancing adjustment entry when
        debit and credit sums differ, posts the move, and reconciles
        the debit/credit payslip lines.
        """
        if not self._need_accounting_entry():
            return True

        Move = self.env["account.move"]
        ML = self.env["account.move.line"]

        currency = self.company_id.currency_id or self.journal_id.company_id.currency_id
        move = Move.create(self._prepare_account_move_data())
        self.move_id = move.id
        debit_sum, credit_sum = self.line_ids.create_move_line(move)

        if currency.compare_amounts(credit_sum, debit_sum) == -1:
            move_line = ML.create(
                self._prepare_adjustment_aml_data(
                    currency, credit_sum, debit_sum, move, "credit"
                )
            )
            self.move_line_credit_id = move_line.id
        elif currency.compare_amounts(debit_sum, credit_sum) == -1:
            move_line = ML.create(
                self._prepare_adjustment_aml_data(
                    currency, credit_sum, debit_sum, move, "debit"
                )
            )
            self.move_line_debit_id = move_line.id

        move.action_post()
        self._reconcile_debit_payslip_line()
        self._reconcile_credit_payslip_line()

    def _compute_payslip(self):
        """Recompute this payslip's salary rule results.

        Deletes the current ``line_ids`` and re-creates them from
        ``_prepare_payslip_line_data``.
        """
        self.ensure_one()
        self.line_ids.unlink()
        self.write(self._prepare_payslip_line_data())

    def _recompute_allowance_ref(self):
        """Refresh ``allowance_ref_move_line_ids`` from eligible lines.

        Re-searches ``allowed_allowance_move_line_ids`` restricted to
        the payslip's ``date_start`` / ``date_end`` window and writes
        the matches back to ``allowance_ref_move_line_ids``.
        """
        self.ensure_one()
        ML = self.env["account.move.line"]
        criteria = [
            "&",
            "|",
            "&",
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            "&",
            ("date_maturity", ">=", self.date_start),
            ("date_maturity", "<=", self.date_end),
            ("id", "in", self.allowed_allowance_move_line_ids.ids),
        ]
        move_lines = ML.search(criteria)
        self.write({"allowance_ref_move_line_ids": [(6, 0, move_lines.ids)]})

    def _recompute_deduction_ref(self):
        """Refresh ``deduction_ref_move_line_ids`` from eligible lines.

        Re-searches ``allowed_deduction_move_line_ids`` restricted to
        the payslip's ``date_start`` / ``date_end`` window and writes
        the matches back to ``deduction_ref_move_line_ids``.
        """
        self.ensure_one()
        ML = self.env["account.move.line"]
        criteria = [
            "&",
            "|",
            "&",
            "&",
            ("date_maturity", "=", False),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            "&",
            ("date_maturity", ">=", self.date_start),
            ("date_maturity", "<=", self.date_end),
            ("id", "in", self.allowed_deduction_move_line_ids.ids),
        ]
        move_lines = ML.search(criteria)
        self.write({"deduction_ref_move_line_ids": [(6, 0, move_lines.ids)]})

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        """Extend the multiple-approval policy fields for payslips.

        Adds this model's workflow policy fields (``confirm_ok``,
        ``approve_ok``, ``done_ok``, ``cancel_ok``, ``reject_ok``,
        ``restart_ok``, ``restart_approval_ok``,
        ``manual_number_ok``) to the ones returned by the mixin, so
        the multiple approval framework can build the related
        boolean fields and view elements.

        :return: list of policy field names
        """
        res = super(HrPayslip, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _prepare_payslip_line_data(self):
        """Build the ``line_ids`` create commands for this payslip.

        :return: dict with a single ``line_ids`` key of ``(0, 0,
            vals)`` commands, one per rule returned by
            ``_get_payslip_lines``
        """
        self.ensure_one()
        lines = [(0, 0, line) for line in self._get_payslip_lines(self.id)]
        return {"line_ids": lines}

    def _prepare_account_move_data(self):
        """Build the ``account.move`` values for this payslip.

        Extension point: override in a glue module to add analytic
        or operating unit fields without touching
        ``_10_create_accounting_entry``.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        name = _("Payslip of %s") % (self.employee_id.name)
        data = {
            "narration": name,
            "ref": self.name,
            "name": self.name,
            "journal_id": self.journal_id.id,
            "date": self.date or self.date_to,
        }
        return data

    def _prepare_adjustment_aml_data(
        self, currency, credit_sum, debit_sum, move_id, type_data
    ):
        """Build the balancing ``account.move.line`` for this payslip.

        Used when the debit and credit sums of the payslip lines do
        not match, so the journal entry still balances.

        :param currency: currency used to round the adjustment
        :param credit_sum: total credit amount already posted
        :param debit_sum: total debit amount already posted
        :param move_id: the ``account.move`` the line will belong to
        :param type_data: ``"debit"`` to post the adjustment as a
            debit, anything else posts it as a credit
        :return: dict of ``account.move.line`` values
        :raises UserError: if the payslip's journal has no default
            account configured
        """
        self.ensure_one()
        journal_acc_id = self.journal_id.default_account_id.id
        if not journal_acc_id:
            msgError = _(
                "The Expense Journal %s has not properly "
                "configured the Credit or Debit Account!"
            )
            raise UserError(msgError % (self.journal_id.name))

        data = {
            "move_id": move_id.id,
            "name": _("Adjustment Entry"),
            "partner_id": False,
            "account_id": journal_acc_id,
            "journal_id": self.journal_id.id,
            "date": self.date,
        }
        if type_data == "debit":
            data["debit"] = currency.round(credit_sum - debit_sum)
            data["credit"] = 0.0
        else:
            data["credit"] = currency.round(debit_sum - credit_sum)
            data["debit"] = 0.0
        return data

    def _sum_salary_rule_category(self, localdict, category, amount):
        """Add ``amount`` to ``category`` and to its ancestor categories.

        Mutates ``localdict["categories"]`` in place, recursing
        through ``category.parent_id`` first so parent totals include
        every descendant category's amount.

        :param localdict: evaluation context built by
            ``_get_base_localdict``
        :param category: the ``hr.salary_rule_category`` the amount
            belongs to
        :param amount: amount to add to the category subtotal
        :return: the same ``localdict``, for convenience
        """
        self.ensure_one()
        if category.parent_id:
            localdict = self._sum_salary_rule_category(
                localdict, category.parent_id, amount
            )

        if category.code in localdict["categories"].dict:
            localdict["categories"].dict[category.code] += amount
        else:
            localdict["categories"].dict[category.code] = amount

        return localdict

    def _get_salary_rules(self):
        """Return this payslip's applicable rules, sequence-sorted.

        Expands ``structure_id`` and its ancestors through
        ``hr.salary_structure._get_parent_structure`` /
        ``get_all_rules``.

        :return: ``hr.salary_rule`` recordset sorted by ``sequence``
        """
        self.ensure_one()
        obj_hr_salary_rule = self.env["hr.salary_rule"]
        obj_hr_salary_struc = self.env["hr.salary_structure"]
        rule_ids = []
        if self.structure_id.id:
            structure_ids = obj_hr_salary_struc.browse(
                self.structure_id.id
            )._get_parent_structure()
            rule_ids = structure_ids.get_all_rules()
            sorted_rule_ids = [
                id for id, sequence in sorted(rule_ids, key=lambda x: x[1])
            ]
            rule_ids = obj_hr_salary_rule.browse(sorted_rule_ids)
        return rule_ids

    def _get_base_localdict(self, payslip):
        """Build the evaluation context shared by every salary rule.

        The returned dict is the localdict later passed to
        ``hr.salary_rule._evaluate_rule`` (and, through it, to
        ``safe_eval``) while computing ``payslip``. It exposes:

        * ``env`` -- the current Odoo environment
        * ``time`` / ``datetime`` / ``dateutil`` / ``timezone`` --
          date/time helpers
        * ``float_compare`` / ``UserError`` -- helper callables
        * ``categories`` -- running per-category totals, mutated by
          ``_sum_salary_rule_category``
        * ``inputs`` -- this payslip's ``hr.payslip_input`` lines,
          keyed by input type ``code``
        * ``emp_inputs`` -- the employee's ``hr.employee_input``
          lines, keyed by input type ``code``
        * ``payslip`` -- helper exposing ``sum()`` over past payslips
        * ``rules`` -- running per-rule totals, keyed by rule ``code``

        :param payslip: the ``hr.payslip`` being computed
        :return: dict evaluation context (localdict)
        """
        self.ensure_one()
        inputs_dict = {}
        emp_inputs_dict = {}
        baselocaldict = {
            "env": self.env,
            "time": tools.safe_eval.time,
            "datetime": tools.safe_eval.datetime,
            "dateutil": tools.safe_eval.dateutil,
            "timezone": timezone,
            "float_compare": float_compare,
            "UserError": odoo.exceptions.UserError,
        }

        categories = BrowsableObject(payslip.employee_id.id, {}, self.env)
        if categories:
            baselocaldict["categories"] = categories

        for input_line in self.input_line_ids:
            inputs_dict[input_line.input_type_id.code] = input_line
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        if inputs:
            baselocaldict["inputs"] = inputs

        for emp_input_line in self.employee_id.input_line_ids:
            emp_inputs_dict[emp_input_line.input_type_id.code] = emp_input_line
        emp_inputs = EmployeeInputLine(
            payslip.employee_id.id, emp_inputs_dict, self.env
        )
        if emp_inputs:
            baselocaldict["emp_inputs"] = emp_inputs

        payslips = Payslips(payslip.employee_id.id, self, self.env)
        if payslips:
            baselocaldict["payslip"] = payslips

        rules = BrowsableObject(payslip.employee_id.id, {}, self.env)
        if rules:
            baselocaldict["rules"] = rules

        return baselocaldict

    @api.model
    def _get_payslip_lines(self, payslip_id):
        """Evaluate every applicable rule and build payslip line data.

        For each rule returned by ``_get_salary_rules``, seeds
        ``localdict["result"]`` / ``["result_qty"]`` /
        ``["result_rate"]``, evaluates the rule's condition and, when
        it applies, its amount; both are read back from ``localdict``
        after ``hr.salary_rule._evaluate_rule`` runs the rule's
        Python code through ``safe_eval``. Rules whose condition is
        false blacklist their descendants (via
        ``_recursive_search_of_rules``) so they are skipped too.

        :param payslip_id: id of the ``hr.payslip`` being computed
        :return: list of ``hr.payslip_line`` value dicts, one per
            applied rule
        """
        self.ensure_one()
        result_dict = {}
        rules_dict = {}
        blacklist = []

        obj_hr_payslip = self.env["hr.payslip"]

        employee = self.employee_id

        payslip = obj_hr_payslip.browse(payslip_id)

        baselocaldict = self._get_base_localdict(payslip)

        sorted_rules = self._get_salary_rules()

        localdict = dict(baselocaldict, employee=employee)
        for rule in sorted_rules:
            key = rule.code
            localdict["result"] = None
            localdict["result_qty"] = 1.0
            localdict["result_rate"] = 100
            if rule._evaluate_rule("condition", localdict) and rule.id not in blacklist:
                amount, qty, rate = rule._evaluate_rule("amount", localdict)
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                tot_rule = amount * qty * rate / 100.0
                localdict[rule.code] = tot_rule
                rules_dict[rule.code] = rule
                localdict = self._sum_salary_rule_category(
                    localdict, rule.category_id, tot_rule - previous_amount
                )
                result_dict[key] = {
                    "payslip_id": payslip_id,
                    "rule_id": rule.id,
                    "amount": amount,
                    "quantity": qty,
                    "rate": rate,
                }
            else:
                blacklist += [id for id, seq in rule._recursive_search_of_rules()]

        return list(result_dict.values())

    def _get_input_line_ids(self):
        """Resolve the input types expected by this payslip's structure.

        Expands ``structure_id`` and its ancestors to the sorted list
        of applicable rules, then collects their ``input_type_ids``.

        :return: list of dicts with a single ``input_type_id`` key,
            one per distinct ``hr.payslip_input_type``
        """
        self.ensure_one()
        res = []
        obj_hr_salary_struc = self.env["hr.salary_structure"]
        obj_hr_salary_rule = self.env["hr.salary_rule"]

        structure_id = self.structure_id.id

        structure_ids = obj_hr_salary_struc.browse(structure_id)._get_parent_structure()
        rule_ids = structure_ids.get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        input_type_ids = obj_hr_salary_rule.browse(sorted_rule_ids).mapped(
            "input_type_ids"
        )
        for input_type in input_type_ids:
            res.append(
                {
                    "input_type_id": input_type.id,
                }
            )
        return res

    def _reload_input_lines(self):
        """Rebuild ``input_line_ids`` by re-running the structure onchange.

        Thin wrapper around ``onchange_input_line_ids`` so it can be
        called outside of an onchange context (e.g. from
        ``action_reload_input_lines``).
        """
        self.ensure_one()
        self.onchange_input_line_ids()

    def _reconcile_debit_payslip_line(self):
        """Reconcile every line whose rule has ``reconcile_debit`` set.

        Delegates to ``hr.payslip_line._reconcile_debit`` for each
        matching ``line_ids`` record.
        """
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]
        criteria = [
            ("payslip_id", "=", self.id),
            ("rule_id.reconcile_debit", "=", True),
        ]
        for detail in PayslipLine.search(criteria):
            detail._reconcile_debit()

    def _reconcile_credit_payslip_line(self):
        """Reconcile every line whose rule has ``reconcile_credit`` set.

        Delegates to ``hr.payslip_line._reconcile_credit`` for each
        matching ``line_ids`` record.
        """
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]
        criteria = [
            ("payslip_id", "=", self.id),
            ("rule_id.reconcile_credit", "=", True),
        ]
        for detail in PayslipLine.search(criteria):
            detail._reconcile_credit()
