# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrPayslipBatch(models.Model):
    _name = "hr.payslip_batch"
    _description = "Employee Payslip Batch"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
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

    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.payslip_type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Batch Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
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
            draft_payslip_ids.action_confirm()
            _check_state = document._check_payslip_state(["draft"])
            if _check_state:
                return _super.action_confirm()

    def action_approve_approval(self):
        _super = super(HrPayslipBatch, self)
        for document in self.sudo():
            confirm_payslip_ids = document.payslip_ids.filtered(
                lambda x: x.state == "confirm"
            )
            confirm_payslip_ids.action_approve_approval()
            _check_state = document._check_payslip_state(["confirm"])
            if _check_state:
                return _super.action_approve_approval()

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
            cancel_payslip_ids.action_cancel(cancel_reason)
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
            cancel_payslip_ids.action_restart()
            _check_state = document._check_payslip_state(["cancel", "reject"])
            if _check_state:
                return _super.action_restart()
