# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
{
    "name": "Employee Payslip Batch",
    "version": "14.0.2.8.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_payroll",
        "ssi_transaction_open_mixin",
        "ssi_accounting_entry_mixin",
        "ssi_company_currency_mixin",
        "ssi_m2o_configurator_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "views/hr_payslip_batch_input_import_views.xml",
        "views/hr_payslip_batch_views.xml",
        "views/hr_payslip_views.xml",
        "views/assets.xml",
    ],
    "demo": [],
    "images": [],
    "external_dependencies": {
        "python": ["openpyxl", "xlsxwriter"],
    },
}
