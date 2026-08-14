# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee Payslip + Operating Unit",
    "version": "14.0.2.0.4",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_payroll",
        "ssi_operating_unit_mixin",
        "ssi_financial_accounting_operating_unit",
        "web_tour",
    ],
    "data": [
        "security/res_group/res_group_data.xml",
        "security/ir_rule/ir_rule_data.xml",
        "views/hr_payslip_views.xml",
        "views/assets.xml",
    ],
}
