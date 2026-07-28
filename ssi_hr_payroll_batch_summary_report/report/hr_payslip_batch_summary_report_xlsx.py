# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, models


class HrPayslipBatchSummaryReportXlsx(models.AbstractModel):
    """
    Renders the Salary Summary report as an ``.xlsx`` workbook.
    Reuses the aggregation logic of ``batch_summary`` (the HTML report
    model) and lays out one worksheet per ``hr.payslip_batch``.
    """

    _name = "report.ssi_hr_payroll_batch_summary_report.batch_summary_xlsx"
    _description = "Payslip Batch Salary Summary XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, batches):
        """Write one Salary Summary worksheet per batch into workbook.

        Override of the ``report.report_xlsx.abstract`` contract
        method. For each batch, adds a worksheet (named after the
        batch, truncated to 31 characters) with a title/period header,
        one column per salary rule used in the batch, one row per
        payslip (linked to the payslip form), and a totals row.

        :param workbook: ``xlsxwriter.Workbook`` to write the report
            into; formats and worksheets are added directly on it
        :param data: unused, present for the abstract report contract
        :param batches: ``hr.payslip_batch`` recordset to render
        :return: ``None`` — output is the side effect of writing to
            ``workbook``
        """
        report_obj = self.env[
            "report.ssi_hr_payroll_batch_summary_report.batch_summary"
        ]

        # Workbook formats
        fmt_title = workbook.add_format(
            {"bold": True, "font_size": 13, "align": "left"}
        )
        fmt_subtitle = workbook.add_format(
            {"bold": True, "font_size": 11, "align": "left"}
        )
        fmt_info = workbook.add_format({"font_size": 10})
        fmt_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#C6EFCE",
                "text_wrap": True,
                "font_size": 9,
            }
        )
        fmt_cell_center = workbook.add_format(
            {"border": 1, "align": "center", "font_size": 9, "valign": "vcenter"}
        )
        fmt_amount = workbook.add_format(
            {
                "border": 1,
                "num_format": "#,##0",
                "align": "right",
                "font_size": 9,
                "valign": "vcenter",
            }
        )
        fmt_total_label = workbook.add_format(
            {"bold": True, "border": 1, "font_size": 9, "bg_color": "#FFFFCC"}
        )
        fmt_total_amount = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "num_format": "#,##0",
                "align": "right",
                "font_size": 9,
                "bg_color": "#FFFFCC",
            }
        )
        fmt_link = workbook.add_format(
            {
                "border": 1,
                "font_color": "#0000EE",
                "underline": True,
                "font_size": 9,
                "valign": "vcenter",
            }
        )

        for batch in batches:
            rules = report_obj._get_salary_rules(batch)
            rule_list = list(rules)

            # 2 fixed cols (No, Nama) + N rule cols + 1 total col
            total_cols = 2 + len(rule_list) + 1

            sheet_name = (batch.name or _("Salary Summary"))[:31]
            sheet = workbook.add_worksheet(sheet_name)

            # --- Column widths ---
            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 38)
            for i in range(len(rule_list)):
                sheet.set_column(2 + i, 2 + i, 16)
            sheet.set_column(2 + len(rule_list), 2 + len(rule_list), 16)

            # --- Header rows ---
            row = 0

            company_name = batch.company_id.name or ""
            batch_month = ""
            if batch.date:
                batch_month = batch.date.strftime("%B %Y").upper()

            title_text = "{} - {}".format(
                _("SALARY SUMMARY %s") % company_name, batch_month
            )
            sheet.merge_range(row, 0, row, total_cols - 1, title_text, fmt_title)
            row += 1

            if batch.analytic_account_id:
                sheet.merge_range(
                    row,
                    0,
                    row,
                    total_cols - 1,
                    batch.analytic_account_id.name,
                    fmt_subtitle,
                )
                row += 1

            period_text = _("Period: %s s/d %s") % (
                batch.date_start.strftime("%d/%m/%Y") if batch.date_start else "",
                batch.date_end.strftime("%d/%m/%Y") if batch.date_end else "",
            )
            sheet.merge_range(row, 0, row, total_cols - 1, period_text, fmt_info)
            row += 2

            # --- Column headers ---
            sheet.set_row(row, 30)
            sheet.write(row, 0, _("No"), fmt_header)
            sheet.write(row, 1, _("Employee Name"), fmt_header)
            for i, rule in enumerate(rule_list):
                sheet.write(row, 2 + i, rule.name, fmt_header)
            sheet.write(row, 2 + len(rule_list), _("Total"), fmt_header)
            row += 1

            # --- Data rows ---
            rule_totals = {rule.id: 0.0 for rule in rule_list}
            grand_total = 0.0

            for seq, payslip in enumerate(batch.payslip_ids.sorted("id"), 1):
                amounts = report_obj._get_amounts_by_rule(payslip)
                row_total = sum(amounts.values())
                grand_total += row_total

                sheet.write(row, 0, seq, fmt_cell_center)

                payslip_url = "/web#id={}&model=hr.payslip&view_type=form".format(
                    payslip.id
                )
                sheet.write_url(
                    row,
                    1,
                    payslip_url,
                    fmt_link,
                    payslip.employee_id.name or "",
                )

                for i, rule in enumerate(rule_list):
                    amt = amounts.get(rule.id, 0.0)
                    rule_totals[rule.id] += amt
                    sheet.write_number(row, 2 + i, amt, fmt_amount)

                sheet.write_number(row, 2 + len(rule_list), row_total, fmt_amount)
                row += 1

            # --- Totals row ---
            sheet.write(row, 0, "", fmt_total_label)
            sheet.write(row, 1, _("Total"), fmt_total_label)
            for i, rule in enumerate(rule_list):
                sheet.write_number(row, 2 + i, rule_totals[rule.id], fmt_total_amount)
            sheet.write_number(row, 2 + len(rule_list), grand_total, fmt_total_amount)
