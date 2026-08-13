# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
{
    "name": "Employee Payslip Batch - Salary Summary Report",
    "version": "14.0.1.1.4",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_payroll_batch",
        "report_xlsx",
        "web_tour",
    ],
    "data": [
        "report/templates/hr_payslip_batch_summary_report.xml",
        "reports.xml",
        "views/hr_payslip_batch_views.xml",
        "views/assets.xml",
    ],
    "demo": [],
    "images": [],
}
