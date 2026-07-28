# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrPayslip(models.Model):
    """
    Enables ``hr.work_log`` tracking on the payslip.

    Adds ``mixin.work_object`` to ``hr.payslip`` so payroll clerks can
    estimate and record work logs (e.g. outsourced or ad-hoc work)
    directly against a payslip, and turns on the mixin's automatic
    ``Work Log`` form tab (``_work_log_create_page``) so the tab
    renders without any additional view inheritance.
    """

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "mixin.work_object",
    ]

    _work_log_create_page = True
