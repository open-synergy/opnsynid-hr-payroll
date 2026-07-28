# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class HrPayslipBatch(models.Model):
    """
    Adds the Salary Summary report actions to the payslip batch.
    Exposes both the printable HTML report and the ``.xlsx`` export
    defined by ``ssi_hr_payroll_batch_summary_report``.
    """

    _inherit = "hr.payslip_batch"

    def action_print_salary_summary(self):
        """Open the Salary Summary report as a printable HTML document.

        Triggered from the batch form button. Delegates to the
        ``ir.actions.report`` registered as
        ``action_report_hr_payslip_batch_summary_html``.

        :return: an ``ir.actions.report`` action dict for this batch
        """
        self.ensure_one()
        return self.env.ref(
            "ssi_hr_payroll_batch_summary_report"
            ".action_report_hr_payslip_batch_summary_html"
        ).report_action(self)

    def action_export_salary_summary_xlsx(self):
        """Export the Salary Summary report as an ``.xlsx`` file.

        Triggered from the batch form button. Delegates to the
        ``ir.actions.report`` registered as
        ``action_report_hr_payslip_batch_summary_xlsx``.

        :return: an ``ir.actions.report`` action dict for this batch
        """
        self.ensure_one()
        return self.env.ref(
            "ssi_hr_payroll_batch_summary_report"
            ".action_report_hr_payslip_batch_summary_xlsx"
        ).report_action(self)
