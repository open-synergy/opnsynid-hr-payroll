# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class HrPayslip(models.Model):
    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
    ]

    @api.depends("employee_id", "date_start", "date_end")
    def _compute_computation_ids(self):
        Timesheet = self.env["hr.timesheet"]
        for payslip in self:
            computation_ids = []
            criteria = [
                ("employee_id", "=", payslip.employee_id.id),
                ("date_start", ">=", payslip.date_start),
                ("date_end", "<=", payslip.date_end),
                ("state", "=", "done"),
            ]
            timesheets = Timesheet.search(criteria)
            for timesheet in timesheets:
                computation_ids += timesheet.computation_ids.ids
            payslip.timesheet_computation_ids = [(6, 0, computation_ids)]

    timesheet_computation_ids = fields.Many2many(
        string="Timesheet Computations",
        comodel_name="hr.timesheet_computation",
        compute="_compute_computation_ids",
        compute_sudo=True,
    )
