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
        "company_id",
    )
    def _compute_employee_ids(self):
        obj_employee = self.env["hr.employee"]
        for document in self:
            criteria = [
                ("salary_structure_id", "!=", False),
            ]
            employee_ids = obj_employee.search(criteria)
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
        result = payslip._prepare_payslip_line_data()
        result["batch_id"] = self.id
        return result

    def _trigger_onchange(self, payslip):
        self.ensure_one()
        payslip.onchange_input_line_ids()
        payslip.onchange_department_id()
        payslip.onchange_manager_id()
        payslip.onchange_job_id()

    def _generate_payslip(self):
        self.ensure_one()
        obj_hr_payslip = self.env["hr.payslip"]
        if not self.payslip_ids:
            for employee in self.employee_ids:
                payslip = obj_hr_payslip.create(self._prepare_payslip_data(employee))
                self._trigger_onchange(payslip)
                payslip.write(self._prepare_payslip_batch_line_data(payslip))

    def _check_payslip_state(self, list_state):
        self.ensure_one()
        result = False
        state_payslip_ids = self.payslip_ids.filtered(lambda x: x.state in list_state)
        if len(state_payslip_ids.ids) == 0:
            result = True
        return result

    def action_compute_payslip(self):
        for document in self.sudo():
            draft_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state == "draft"
            )
            for payslip in draft_payslip_ids:
                payslip.action_compute_payslip()

    def action_reload_employee(self):
        for record in self.sudo():
            record._reload_employee()

    def _reload_employee(self):
        self.ensure_one()
        self.write({"employee_ids": [(6, 0, self.allowed_employee_ids.ids)]})

    def _get_batch_input_type_ids(self):
        """Return all distinct payslip input types used across every payslip
        of this batch, sorted by their code. These become the dynamic input
        columns of the export/import spreadsheet."""
        self.ensure_one()
        input_type_ids = self.payslip_ids.mapped("input_line_ids.input_type_id")
        return input_type_ids.sorted(key=lambda record: (record.code or "", record.id))

    def _prepare_input_export_filename(self):
        self.ensure_one()
        name = self.name and self.name != "/" and self.name or str(self.id)
        return "payslip_batch_input_%s.xlsx" % name

    def action_export_input(self):
        """Generate an xlsx file containing, for every payslip of the batch,
        its database ID, the employee name, and one dynamic column per input
        code present in the batch. The cell value is the input amount."""
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
        self.ensure_one()
        result = True
        if not self.employee_ids:
            result = False
        return result

    def action_confirm(self):
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
        """Record batch approval. Payslips are driven to done in _05_done_payslip."""
        return super(HrPayslipBatch, self).action_approve_approval()

    def action_reject_approval(self):
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
        self.ensure_one()
        if not self.move_id:
            return True
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
        self.account_entry_ids.unlink()

    # -- aggregation helpers --

    def _prepare_batch_account_entries(self):
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
        self.ensure_one()
        return self.payslip_ids.mapped("allowance_ref_move_line_ids")

    def _get_batch_deduction_ref_ml(self):
        self.ensure_one()
        return self.payslip_ids.mapped("deduction_ref_move_line_ids")

    def _reconcile_batch_account_entry(self):
        self.ensure_one()
        allowance = self._get_batch_allowance_ref_ml()
        deduction = self._get_batch_deduction_ref_ml()
        for entry in self.account_entry_ids:
            if entry.rule_id.reconcile_debit and entry.debit_move_line_id:
                entry._reconcile_debit(allowance)
            if entry.rule_id.reconcile_credit and entry.credit_move_line_id:
                entry._reconcile_credit(deduction)

    def _unreconcile_batch_account_entry(self):
        self.ensure_one()
        for entry in self.account_entry_ids:
            if entry.debit_move_line_id:
                entry.debit_move_line_id.remove_move_reconcile()
            if entry.credit_move_line_id:
                entry.credit_move_line_id.remove_move_reconcile()
