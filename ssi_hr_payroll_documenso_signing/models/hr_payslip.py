# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrPayslip(models.Model):  # pylint: disable=R0903
    """
    Enables Documenso-based signing for the payslip approval flow.

    Adds the approval-aware Documenso signing tab to ``hr.payslip`` via
    ``mixin.documenso_signing_approval``, so a payslip approval template
    with a ``documenso_signing_template_id`` is satisfied by a single
    external ``documenso.signature.request`` instead of individual
    in-app approvers.
    """

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
