# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrPayslipBatch(models.Model):
    """
    Adds work log tracking to payslip batches.
    Activates the Work Log tab on the ``hr.payslip_batch`` form via
    ``mixin.work_object``, so hours logged while processing a batch
    are recorded against ``work_estimation`` and rolled up into
    ``total_work``, ``remaining_work``, and ``excess_work``.
    """

    _name = "hr.payslip_batch"
    _inherit = [
        "hr.payslip_batch",
        "mixin.work_object",
    ]

    _work_log_create_page = True
