# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee Payslip Batch + Operating Unit",
    "version": "14.0.1.5.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_payroll_batch",
        "ssi_hr_payroll_operating_unit",
        "ssi_hr_employee_operating_unit",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/res_group_data.xml",
        "security/ir_rule/ir_rule_data.xml",
        "views/hr_payslip_batch_views.xml",
        "views/assets.xml",
    ],
}
