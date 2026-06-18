# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class HrPayslipBatch(models.Model):
    _inherit = "hr.payslip_batch"

    def action_print_salary_summary(self):
        self.ensure_one()
        return self.env.ref(
            "ssi_hr_payroll_batch_summary_report"
            ".action_report_hr_payslip_batch_summary_html"
        ).report_action(self)

    def action_export_salary_summary_xlsx(self):
        self.ensure_one()
        return self.env.ref(
            "ssi_hr_payroll_batch_summary_report"
            ".action_report_hr_payslip_batch_summary_xlsx"
        ).report_action(self)
