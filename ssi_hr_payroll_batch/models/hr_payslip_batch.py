# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import io

import xlsxwriter

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator
from odoo.addons.ssi_hr_payroll.models.hr_payslip_type import ACCOUNTING_METHOD


class HrPayslipBatch(models.Model):
    """
    Group multiple employee payslips into one batch that shares a single
    approval workflow (draft/open/confirm/done/cancel/reject).

    Opening the batch generates one ``hr.payslip`` per selected employee.
    Confirming, approving, cancelling, or restarting the batch drives all
    its payslips through the same transition, so an employee's payslip
    can never be individually out of sync with the batch (see
    ``hr.payslip._check_batch_lock``). When ``accounting_method`` is
    ``'batch'``, journal entries of the individual payslip lines are
    aggregated per (rule, partner) into
    ``hr.payslip_batch_account_entry`` and posted as a single
    ``account.move`` instead of one move per payslip.
    """

    _name = "hr.payslip_batch"
    _description = "Employee Payslip Batch"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
        "mixin.account_move",
        "mixin.company_currency",
        "mixin.many2one_configurator",
    ]
    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = True
    _automatically_insert_open_button = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,open,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "open_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
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

    # mixin.account_move config
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "move_id"
    _accounting_date_field_name = "date"
    _number_field_name = "name"
    _currency_id_field_name = "company_currency_id"
    _company_currency_id_field_name = "company_currency_id"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.payslip_type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    accounting_method = fields.Selection(
        string="Accounting Method",
        selection=ACCOUNTING_METHOD,
        default="payslip",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Controls where the journal entry is created. "
        "'Journal at Payslip' (default): each payslip creates its own entry. "
        "'Journal at Batch': a single aggregated entry is created for the whole batch.",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Accounting journal for the batch-level journal entry. "
        "Required when Accounting Method is 'Journal at Batch'.",
    )
    move_id = fields.Many2one(
        string="# Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    move_line_debit_id = fields.Many2one(
        string="Move Line Debit (Adjustment)",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    move_line_credit_id = fields.Many2one(
        string="Move Line Credit (Adjustment)",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    account_entry_ids = fields.One2many(
        string="Account Entries",
        comodel_name="hr.payslip_batch_account_entry",
        inverse_name="batch_id",
        readonly=True,
        copy=False,
        help="Aggregated (rule, partner) journal entries for this batch "
        "(only populated when Accounting Method is 'Journal at Batch').",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Analytic account used for journal items of payslips in this batch.",
    )
    debit_usage_id = fields.Many2one(
        string="Debit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Product usage type used to resolve the debit account "
        "of this payslip batch.",
    )
    credit_usage_id = fields.Many2one(
        string="Credit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Product usage type used to resolve the credit account "
        "of this payslip batch.",
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
    date = fields.Date(
        string="Batch Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Date of the payslip batch.",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_accounting_method(self):
        self.accounting_method = "payslip"
        if self.type_id:
            self.accounting_method = self.type_id.accounting_method

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
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False
        if self.type_id:
            self.analytic_account_id = self.type_id.analytic_account_id

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

    @api.constrains("accounting_method", "journal_id")
    def _check_batch_journal_id_required(self):
        """Ensure ``journal_id`` is set when journaling at batch level.

        :raises ValidationError: if ``accounting_method`` is ``'batch'``
            and ``journal_id`` is empty.
        """
        for record in self:
            if record.accounting_method == "batch" and not record.journal_id:
                raise ValidationError(
                    _(
                        """
Context: Validate payslip batch accounting configuration
Database ID: %s
Problem: Journal is required when Accounting Method is 'Journal at Batch'
Solution: Set a journal on the batch, or change the Accounting Method to 'Journal at Payslip'
                    """
                    )
                    % (record.id,)
                )

    @api.depends(
        "type_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        """Compute ``allowed_analytic_account_ids`` from the payslip type.

        Resolves the M2O configurator filter (manual/domain/code)
        defined on ``type_id`` for the analytic account. Falls back to
        every ``account.analytic.account`` record when ``type_id`` is
        not yet set, so the field stays usable while the batch is
        being filled in.
        """
        # No type_id yet (e.g. the batch is still being filled in on a new
        # record): behave like the type's own "no restriction" default
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
        """Compute ``allowed_debit_usage_ids`` from the payslip type.

        Resolves the M2O configurator filter (manual/domain/code)
        defined on ``type_id`` for the debit usage. Falls back to
        every ``product.usage_type`` record when ``type_id`` is not
        yet set, so the field stays usable while the batch is being
        filled in.
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
        """Compute ``allowed_credit_usage_ids`` from the payslip type.

        Resolves the M2O configurator filter (manual/domain/code)
        defined on ``type_id`` for the credit usage. Falls back to
        every ``product.usage_type`` record when ``type_id`` is not
        yet set, so the field stays usable while the batch is being
        filled in.
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
        "company_id",
        "type_id",
    )
    def _compute_employee_ids(self):
        """Compute ``allowed_employee_ids`` for this batch.

        Starts from every ``hr.employee`` with a salary structure
        assigned, then narrows it down with the M2O configurator
        filter defined on ``type_id`` (when set) to obtain the
        employees that may be added to ``employee_ids``.
        """
        obj_employee = self.env["hr.employee"]
        for document in self:
            criteria = [
                ("salary_structure_id", "!=", False),
            ]
            employee_ids = obj_employee.search(criteria)
            if document.type_id:
                configurator_employee_ids = document._m2o_configurator_get_filter(
                    object_name="hr.employee",
                    method_selection=document.type_id.employee_selection_method,
                    manual_recordset=document.type_id.employee_ids,
                    domain=document.type_id.employee_domain,
                    python_code=document.type_id.employee_python_code,
                )
                employee_ids = employee_ids & configurator_employee_ids
            document.allowed_employee_ids = [(6, 0, employee_ids.ids)]

    allowed_employee_ids = fields.Many2many(
        string="Allowed Employees",
        comodel_name="hr.employee",
        compute="_compute_employee_ids",
    )
    employee_ids = fields.Many2many(
        string="Employees",
        comodel_name="hr.employee",
        relation="rel_payslip_batch_2_employee",
        column1="batch_id",
        column2="employee_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    payslip_ids = fields.One2many(
        string="Payslips",
        comodel_name="hr.payslip",
        inverse_name="batch_id",
        readonly=True,
    )
    payslip_count = fields.Integer(
        string="# Payslip",
        compute="_compute_payslip_count",
        help="Number of payslips generated for this batch. "
        "Used to display the payslip count on the 'Open Payslip' smart button.",
    )

    @api.depends(
        "payslip_ids",
    )
    def _compute_payslip_count(self):
        """Compute ``payslip_count`` from the number of ``payslip_ids``."""
        for record in self:
            record.payslip_count = len(record.payslip_ids)

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super(HrPayslipBatch, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _prepare_payslip_data(self, employee):
        """Build the ``hr.payslip`` creation values for ``employee``.

        Extension point: override to add or override default values
        (e.g. company, contract) before the payslip is created by
        ``_generate_payslip``.

        :param employee: ``hr.employee`` record the payslip is for
        :return: dict of ``hr.payslip`` values
        """
        type = self.type_id
        structure_id = employee.salary_structure_id.id
        return {
            "employee_id": employee.id,
            "type_id": type.id,
            "structure_id": structure_id,
            "journal_id": type.journal_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "debit_usage_id": self.debit_usage_id.id,
            "credit_usage_id": self.credit_usage_id.id,
            "date": self.date,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    def _prepare_payslip_batch_line_data(self, payslip):
        """Build the write values applied to a freshly created payslip.

        Delegates to ``payslip._prepare_payslip_line_data`` and stamps
        the result with this batch's ``batch_id``.

        :param payslip: ``hr.payslip`` record just created for an
            employee of this batch
        :return: dict of values to write on ``payslip``
        """
        result = payslip._prepare_payslip_line_data()
        result["batch_id"] = self.id
        return result

    def _trigger_onchange(self, payslip):
        """Replay the onchange methods needed after creating a payslip.

        A payslip created via ``create()`` does not run its form
        onchange methods automatically; this forces
        ``onchange_input_line_ids``, ``onchange_department_id``,
        ``onchange_manager_id``, and ``onchange_job_id`` so ``payslip``
        ends up with the same values as if it had been filled in
        through the UI.

        :param payslip: ``hr.payslip`` record to trigger onchange on
        """
        self.ensure_one()
        payslip.onchange_input_line_ids()
        payslip.onchange_department_id()
        payslip.onchange_manager_id()
        payslip.onchange_job_id()

    def _generate_payslip(self):
        """Create one ``hr.payslip`` per employee of this batch.

        Skipped entirely when ``payslip_ids`` is already populated
        (e.g. batch re-opened after being restarted), so payslips are
        never duplicated. Each created payslip is initialised via
        ``_prepare_payslip_data``, has its onchange replayed with
        ``_trigger_onchange``, then gets its computed lines written
        back via ``_prepare_payslip_batch_line_data``.
        """
        self.ensure_one()
        obj_hr_payslip = self.env["hr.payslip"]
        if not self.payslip_ids:
            for employee in self.employee_ids:
                payslip = obj_hr_payslip.create(self._prepare_payslip_data(employee))
                self._trigger_onchange(payslip)
                payslip.write(self._prepare_payslip_batch_line_data(payslip))

    def _check_payslip_state(self, list_state):
        """Check whether none of this batch's payslips are in ``list_state``.

        Used to gate batch-level state transitions until every
        individual payslip has already left ``list_state`` on its own.

        :param list_state: iterable of payslip state values to check
            against
        :return: ``True`` when no payslip of this batch is in any of
            ``list_state``
        """
        self.ensure_one()
        result = False
        state_payslip_ids = self.payslip_ids.filtered(lambda x: x.state in list_state)
        if len(state_payslip_ids.ids) == 0:
            result = True
        return result

    def action_compute_payslip(self):
        """Trigger salary rule computation on every draft payslip.

        Calls ``action_compute_payslip`` on each payslip of this batch
        currently in ``draft`` state.
        """
        for document in self.sudo():
            draft_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state == "draft"
            )
            for payslip in draft_payslip_ids:
                payslip.action_compute_payslip()

    def action_reload_employee(self):
        """Refresh ``employee_ids`` from the current M2O configurator filter.

        Delegates to ``_reload_employee`` for each record.
        """
        for record in self.sudo():
            record._reload_employee()

    def _reload_employee(self):
        """Replace ``employee_ids`` with ``allowed_employee_ids``."""
        self.ensure_one()
        self.write({"employee_ids": [(6, 0, self.allowed_employee_ids.ids)]})

    def action_open_payslip(self):
        """Open the smart-button window action for this batch's payslips.

        :return: the ``ir.actions.act_window`` dict built by
            ``_open_payslip``
        """
        for record in self.sudo():
            result = record._open_payslip()
        return result

    def _open_payslip(self):
        """Build the window action for this batch's payslips.

        Reuses ``ssi_hr_payroll.hr_payslip_action`` restricted to this
        batch via domain, with the batch pre-filled as default for new
        records.

        :return: an ``ir.actions.act_window`` dict
        """
        self.ensure_one()
        waction = self.env.ref("ssi_hr_payroll.hr_payslip_action").read()[0]
        waction.update(
            {
                "view_mode": "tree,form",
                "domain": [("batch_id", "=", self.id)],
                "context": {"default_batch_id": self.id},
            }
        )
        return waction

    def _get_batch_input_type_ids(self):
        """Return the distinct payslip input types used across this batch.

        Collects every ``hr.payslip_input_type`` referenced by any
        payslip of this batch and sorts it by ``code``. The result
        becomes the dynamic input columns of the export/import
        spreadsheet built by ``action_export_input``.

        :return: ``hr.payslip_input_type`` recordset
        """
        self.ensure_one()
        input_type_ids = self.payslip_ids.mapped("input_line_ids.input_type_id")
        return input_type_ids.sorted(key=lambda record: (record.code or "", record.id))

    def _prepare_input_export_filename(self):
        """Build the filename of the input export spreadsheet.

        :return: filename string, based on ``name`` when the batch is
            already numbered, otherwise on its database ID
        """
        self.ensure_one()
        name = self.name and self.name != "/" and self.name or str(self.id)
        return "payslip_batch_input_%s.xlsx" % name

    def action_export_input(self):
        """Export this batch's payslip inputs to an xlsx attachment.

        Builds one row per payslip with its database ID, employee
        name, and one dynamic column per input code used in the batch
        (see ``_get_batch_input_type_ids``), filled with the input
        amount. The spreadsheet is stored as an ``ir.attachment`` on
        this record and can be re-imported via
        ``import_payslip_batch_input`` after being edited.

        :return: an ``ir.actions.act_url`` dict pointing to the
            generated attachment
        """
        self.ensure_one()
        input_type_ids = self._get_batch_input_type_ids()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet("Payslip Inputs")
        header_format = workbook.add_format({"bold": True})

        headers = ["Payslip ID", "Employee"]
        headers += [input_type.code for input_type in input_type_ids]
        for column, header in enumerate(headers):
            sheet.write(0, column, header, header_format)

        row = 1
        for payslip in self.payslip_ids:
            amount_by_code = {
                line.input_type_id.code: line.amount for line in payslip.input_line_ids
            }
            sheet.write_number(row, 0, payslip.id)
            sheet.write_string(row, 1, payslip.employee_id.name or "")
            for column, input_type in enumerate(input_type_ids, start=2):
                if input_type.code in amount_by_code:
                    sheet.write_number(row, column, amount_by_code[input_type.code])
            row += 1

        workbook.close()
        output.seek(0)
        attachment = self.env["ir.attachment"].create(
            {
                "name": self._prepare_input_export_filename(),
                "datas": base64.b64encode(output.read()),
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "new",
        }

    def action_open(self):
        """Open the batch and generate its payslips.

        Extends the inherited transition: after the state moves to
        ``open``, generates the batch's payslips via
        ``_generate_payslip``.

        :raises UserError: if no employee is selected on the batch
        """
        _super = super(HrPayslipBatch, self)
        res = _super.action_open()
        for document in self.sudo():
            if not document._check_employee_ids():
                error_message = _(
                    """
                Context: Start payslip batch
                Database ID: %s
                Problem: No employees selected
                Solution: Select employees
                """
                    % (document.id)
                )
                raise UserError(error_message)
            else:
                document._generate_payslip()
        return res

    def _check_employee_ids(self):
        """Check whether at least one employee is selected on this batch.

        :return: ``True`` when ``employee_ids`` is not empty
        """
        self.ensure_one()
        result = True
        if not self.employee_ids:
            result = False
        return result

    def action_confirm(self):
        """Confirm the batch after confirming its draft payslips.

        Drives every payslip still in ``draft`` state to ``confirm``
        first, then only calls the inherited transition once none of
        the batch's payslips remain in ``draft``.
        """
        _super = super(HrPayslipBatch, self)
        for document in self.sudo():
            draft_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state == "draft"
            )
            draft_payslip_ids.with_context(from_batch=True).action_confirm()
            _check_state = document._check_payslip_state(["draft"])
            if _check_state:
                return _super.action_confirm()

    def action_approve_approval(self):
        """Record batch approval.

        Payslips are driven to done in ``_05_done_payslip``.
        """
        return super(HrPayslipBatch, self).action_approve_approval()

    def action_reject_approval(self):
        """Reject the batch's approval after rejecting its payslips.

        Drives every payslip still in ``confirm`` state to rejected
        first, then only calls the inherited transition once none of
        the batch's payslips remain in ``confirm``.
        """
        _super = super(HrPayslipBatch, self)
        for document in self.sudo():
            confirm_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state == "confirm"
            )
            confirm_payslip_ids.action_reject_approval()
            _check_state = document._check_payslip_state(["confirm"])
            if _check_state:
                return _super.action_reject_approval()

    def action_cancel(self, cancel_reason=False):
        """Cancel the batch after cancelling its still-open payslips.

        Cancels every payslip in ``draft``, ``open``, ``confirm``, or
        ``done`` state first, then only calls the inherited transition
        once none of the batch's payslips remain in those states.

        :param cancel_reason: ``ssi_transaction_cancel_mixin`` cancel
            reason record propagated to each payslip
        """
        _super = super(HrPayslipBatch, self)
        for document in self.sudo():
            cancel_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state in ["draft", "open", "confirm", "done"]
            )
            cancel_payslip_ids.with_context(from_batch=True).action_cancel(
                cancel_reason
            )
            _check_state = document._check_payslip_state(
                ["draft", "open", "confirm", "done"]
            )
            if _check_state:
                return _super.action_cancel(cancel_reason)

    def action_restart(self):
        """Restart the batch after restarting its cancelled payslips.

        Restarts every payslip in ``cancel`` or ``reject`` state
        first, then only calls the inherited transition once none of
        the batch's payslips remain in those states.
        """
        _super = super(HrPayslipBatch, self)
        for document in self.sudo():
            cancel_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state in ["cancel", "reject"]
            )
            cancel_payslip_ids.with_context(from_batch=True).action_restart()
            _check_state = document._check_payslip_state(["cancel", "reject"])
            if _check_state:
                return _super.action_restart()

    # -- post_done_action: drive payslips to done first --

    @ssi_decorator.post_done_action()
    def _05_done_payslip(self):
        """Drive all batch payslips to done atomically before journaling."""
        self.ensure_one()
        payslips_to_done = self.payslip_ids.filtered(
            lambda p: p.state not in ["done", "cancel"]
        )
        for payslip in payslips_to_done:
            payslip.with_context(from_batch=True).action_approve_approval()
        not_done = self.payslip_ids.filtered(lambda p: p.state != "done")
        if not_done:
            raise UserError(
                _(
                    """
Context: Process payslip batch to done
Database ID: %s
Problem: %d payslip(s) could not be transitioned to done state
Solution: Check the individual payslip state, approval configuration, \
and required fields
                """
                )
                % (self.id, len(not_done))
            )

    # -- post_done_action: batch journal entry --

    @ssi_decorator.post_done_action()
    def _10_create_accounting_entry(self):
        """Create the batch-level journal entry, when applicable.

        Runs after the batch reaches ``done``. No-op when
        ``accounting_method`` is not ``'batch'``. Otherwise aggregates
        payslip lines into ``account_entry_ids`` (see
        ``_prepare_batch_account_entries``), creates the
        ``account.move`` and its debit/credit lines per entry,
        balances the move with an adjustment line when debit and
        credit totals differ, posts it, and reconciles the batch's
        account entries against the payslips' allowance/deduction
        reference move lines.
        """
        self.ensure_one()
        if self.accounting_method != "batch":
            return True
        self._prepare_batch_account_entries()
        self._create_standard_move()
        debit_sum = 0.0
        credit_sum = 0.0
        for entry in self.account_entry_ids:
            debit_ml, credit_ml = entry._create_standard_ml()
            entry.write(
                {
                    "debit_move_line_id": debit_ml.id if debit_ml else False,
                    "credit_move_line_id": credit_ml.id if credit_ml else False,
                }
            )
            if debit_ml:
                debit_sum += debit_ml.debit - debit_ml.credit
            if credit_ml:
                credit_sum += credit_ml.credit - credit_ml.debit
        self._create_balance_adjustment(debit_sum, credit_sum)
        self._post_standard_move()
        self._reconcile_batch_account_entry()

    # -- post_cancel_action: reverse batch journal entry --

    @ssi_decorator.post_cancel_action()
    def _xx_cancel_accounting_entry(self):
        """Reverse the batch-level journal entry on cancellation.

        Runs after the batch is cancelled. When a ``move_id`` exists,
        unreconciles the batch's account entries, clears their move
        line references (and the batch's adjustment move lines), and
        deletes the standard move. ``account_entry_ids`` are always
        unlinked, even without a move, since they are regenerated from
        scratch by ``_prepare_batch_account_entries`` on the next
        journaling run.
        """
        self.ensure_one()
        if self.move_id:
            self._unreconcile_batch_account_entry()
            self.account_entry_ids.write(
                {
                    "debit_move_line_id": False,
                    "credit_move_line_id": False,
                }
            )
            self.write(
                {
                    "move_line_debit_id": False,
                    "move_line_credit_id": False,
                }
            )
            self._delete_standard_move()
        # Always drop the entries on cancel, even when there is no move (e.g. a
        # batch whose rules are all gate-empty). They are regenerated from scratch
        # by _prepare_batch_account_entries on the next journaling run.
        self.account_entry_ids.unlink()

    # -- aggregation helpers --

    def _prepare_batch_account_entries(self):
        """Rebuild ``account_entry_ids`` by aggregating payslip lines.

        Deletes any existing entries, then groups every non-zero
        payslip line of this batch by ``(rule_id, partner_id)``,
        summing their amounts and resolving the debit/credit account
        of each group. An ``hr.payslip_batch_account_entry`` is
        created for each group whose amount and at least one account
        are set.
        """
        self.ensure_one()
        self.account_entry_ids.unlink()
        lines = self.payslip_ids.mapped("line_ids").filtered(lambda l: l.amount)
        groups = {}
        for line in lines:
            partner_id = line._get_partner_id()
            key = (line.rule_id.id, partner_id)
            debit_acc = line._get_debit_account()
            credit_acc = line._get_credit_account()
            if key not in groups:
                groups[key] = {
                    "rule_id": line.rule_id.id,
                    "partner_id": partner_id or False,
                    "debit_account_id": debit_acc.id if debit_acc else False,
                    "credit_account_id": credit_acc.id if credit_acc else False,
                    "amount": 0.0,
                }
            groups[key]["amount"] += line.amount
        Entry = self.env["hr.payslip_batch_account_entry"]
        for vals in groups.values():
            if vals["amount"] and (
                vals["debit_account_id"] or vals["credit_account_id"]
            ):
                vals["batch_id"] = self.id
                Entry.create(vals)

    def _prepare_balance_adjustment_aml(
        self, currency, credit_sum, debit_sum, move, type_data
    ):
        """Build the values of the adjustment ``account.move.line``.

        :param currency: currency used to round the adjustment amount
        :param credit_sum: total credit posted so far on ``move``
        :param debit_sum: total debit posted so far on ``move``
        :param move: ``account.move`` the adjustment line is added to
        :param type_data: ``'debit'`` to post the adjustment as a
            debit, any other value posts it as a credit
        :raises UserError: if the batch's journal has no default
            account configured
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        journal_acc_id = self.journal_id.default_account_id.id
        if not journal_acc_id:
            raise UserError(
                _(
                    """
Context: Create balance adjustment for payslip batch
Database ID: %s
Problem: Journal '%s' has no default account configured
Solution: Set a default account on the journal, or configure it via \
the accounting journal settings
                """
                )
                % (self.id, self.journal_id.name)
            )
        data = {
            "move_id": move.id,
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

    def _create_balance_adjustment(self, debit_sum, credit_sum):
        """Balance the batch move when debit and credit totals differ.

        Creates a single adjustment ``account.move.line`` (built by
        ``_prepare_balance_adjustment_aml``) on ``move_id`` for the
        difference, storing it on ``move_line_credit_id`` or
        ``move_line_debit_id`` depending on which side is short. Does
        nothing when both totals already match.

        :param debit_sum: total debit posted from the aggregated
            entries
        :param credit_sum: total credit posted from the aggregated
            entries
        """
        self.ensure_one()
        ML = self.env["account.move.line"].with_context(check_move_validity=False)
        currency = self.company_currency_id
        move = self.move_id
        if currency.compare_amounts(credit_sum, debit_sum) == -1:
            ml = ML.create(
                self._prepare_balance_adjustment_aml(
                    currency, credit_sum, debit_sum, move, "credit"
                )
            )
            self.move_line_credit_id = ml.id
        elif currency.compare_amounts(debit_sum, credit_sum) == -1:
            ml = ML.create(
                self._prepare_balance_adjustment_aml(
                    currency, credit_sum, debit_sum, move, "debit"
                )
            )
            self.move_line_debit_id = ml.id

    # -- reconciliation helpers --

    def _get_batch_allowance_ref_ml(self):
        """Return the allowance reference move lines of this batch.

        :return: ``account.move.line`` recordset gathered from every
            payslip's ``allowance_ref_move_line_ids``
        """
        self.ensure_one()
        return self.payslip_ids.mapped("allowance_ref_move_line_ids")

    def _get_batch_deduction_ref_ml(self):
        """Return the deduction reference move lines of this batch.

        :return: ``account.move.line`` recordset gathered from every
            payslip's ``deduction_ref_move_line_ids``
        """
        self.ensure_one()
        return self.payslip_ids.mapped("deduction_ref_move_line_ids")

    def _reconcile_batch_account_entry(self):
        """Reconcile the batch's account entries against payslip references.

        For each ``account_entry_ids`` whose rule requests
        reconciliation, matches its debit move line against the
        batch's allowance reference move lines, and its credit move
        line against the deduction reference move lines, via
        ``hr.payslip_batch_account_entry._reconcile_debit`` /
        ``_reconcile_credit``.
        """
        self.ensure_one()
        allowance = self._get_batch_allowance_ref_ml()
        deduction = self._get_batch_deduction_ref_ml()
        for entry in self.account_entry_ids:
            if entry.rule_id.reconcile_debit and entry.debit_move_line_id:
                entry._reconcile_debit(allowance)
            if entry.rule_id.reconcile_credit and entry.credit_move_line_id:
                entry._reconcile_credit(deduction)

    def _unreconcile_batch_account_entry(self):
        """Undo the reconciliation of the batch's account entries.

        Removes the reconciliation of every ``debit_move_line_id`` and
        ``credit_move_line_id`` present on ``account_entry_ids``.
        Called before the batch's journal entry is deleted on
        cancellation.
        """
        self.ensure_one()
        for entry in self.account_entry_ids:
            if entry.debit_move_line_id:
                entry.debit_move_line_id.remove_move_reconcile()
            if entry.credit_move_line_id:
                entry.credit_move_line_id.remove_move_reconcile()
