# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, models


class HrPayslipBatchSummaryReport(models.AbstractModel):
    _name = "report.ssi_hr_payroll_batch_summary_report.batch_summary"
    _description = "Payslip Batch Salary Summary Report"

    def _get_salary_rules(self, batch):
        """Return salary rules used in this batch, sorted by sequence."""
        SalaryRule = self.env["hr.salary_rule"]
        rule_ids = set()
        for payslip in batch.payslip_ids:
            for line in payslip.line_ids:
                rule_ids.add(line.rule_id.id)
        if not rule_ids:
            return SalaryRule
        return SalaryRule.search([("id", "in", list(rule_ids))], order="sequence, id")

    def _get_amounts_by_rule(self, payslip):
        """Return {rule_id: total} mapping for a payslip."""
        result = {}
        for line in payslip.line_ids:
            result[line.rule_id.id] = line.total
        return result

    def _fmt(self, amount):
        """Format amount in Indonesian style: 1.234.567"""
        formatted = "{:,.0f}".format(abs(float(amount)))
        formatted = formatted.replace(",", ".")
        if float(amount) < 0:
            formatted = "-" + formatted
        return formatted

    @api.model
    def _get_report_values(self, docids, data=None):
        batches = self.env["hr.payslip_batch"].browse(docids)
        docs = []
        for batch in batches:
            rules = self._get_salary_rules(batch)
            payslips_data = []
            rule_totals = {rule.id: 0.0 for rule in rules}
            grand_total = 0.0

            for i, payslip in enumerate(batch.payslip_ids.sorted("id"), 1):
                amounts = self._get_amounts_by_rule(payslip)
                row_total = sum(amounts.values())
                grand_total += row_total

                amounts_fmt = {}
                for rule in rules:
                    amt = amounts.get(rule.id, 0.0)
                    rule_totals[rule.id] += amt
                    amounts_fmt[rule.id] = self._fmt(amt)

                payslips_data.append(
                    {
                        "no": i,
                        "payslip": payslip,
                        "amounts": amounts,
                        "amounts_fmt": amounts_fmt,
                        "total": row_total,
                        "total_fmt": self._fmt(row_total),
                    }
                )

            rule_totals_fmt = {
                rule.id: self._fmt(rule_totals[rule.id]) for rule in rules
            }

            docs.append(
                {
                    "batch": batch,
                    "rules": rules,
                    "payslips": payslips_data,
                    "rule_totals": rule_totals,
                    "rule_totals_fmt": rule_totals_fmt,
                    "grand_total": grand_total,
                    "grand_total_fmt": self._fmt(grand_total),
                }
            )

        return {
            "doc_ids": docids,
            "doc_model": "hr.payslip_batch",
            "docs": docs,
        }
