# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrPayslipBatch(models.Model):  # pylint: disable=R0903
    """
    Adds Documenso-based signing and approval to payslip batches.
    Activates the Documenso tab on the ``hr.payslip_batch`` form and
    replaces the standard multiple-approval flow with a single
    ``documenso.signature.request`` via ``mixin.documenso_signing_approval``:
    the batch is approved once that request is signed, and rejected if a
    signer cancels it in Documenso.
    """

    _name = "hr.payslip_batch"
    _inherit = [
        "hr.payslip_batch",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
