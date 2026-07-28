# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, models


class HrPayslipBatchSummaryReport(models.AbstractModel):
    """
    Builds the values consumed by the Salary Summary QWeb report.
    Aggregates the payslips of one or more ``hr.payslip_batch`` records
    into a per-employee, per-salary-rule breakdown with row and column
    totals, shared by both the HTML report and the ``.xlsx`` export.
    """

    _name = "report.ssi_hr_payroll_batch_summary_report.batch_summary"
    _description = "Payslip Batch Salary Summary Report"

    def _get_salary_rules(self, batch):
        """Return salary rules used in this batch, sorted by sequence.

        :param batch: a single ``hr.payslip_batch`` record
        :return: ``hr.salary_rule`` recordset, ordered by
            ``sequence, id``; empty recordset when the batch has no
            payslips
        """
        SalaryRule = self.env["hr.salary_rule"]
        rule_ids = set()
        for payslip in batch.payslip_ids:
            for line in payslip.line_ids:
                rule_ids.add(line.rule_id.id)
        if not rule_ids:
            return SalaryRule
        return SalaryRule.search([("id", "in", list(rule_ids))], order="sequence, id")

    def _get_amounts_by_rule(self, payslip):
        """Return {rule_id: total} mapping for a payslip.

        :param payslip: a single ``hr.payslip`` record
        :return: dict mapping ``hr.salary_rule`` id to the summed
            ``total`` of that rule's ``hr.payslip_line`` records on
            this payslip
        """
        result = {}
        for line in payslip.line_ids:
            result[line.rule_id.id] = line.total
        return result

    def _fmt(self, amount):
        """Format amount in Indonesian style, e.g. ``1.234.567``.

        :param amount: numeric amount to format
        :return: string with ``.`` as the thousands separator and a
            leading ``-`` for negative amounts
        """
        formatted = "{:,.0f}".format(abs(float(amount)))
        formatted = formatted.replace(",", ".")
        if float(amount) < 0:
            formatted = "-" + formatted
        return formatted

    @api.model
    def _get_report_values(self, docids, data=None):
        """Build the rendering context for the QWeb report engine.

        For each ``hr.payslip_batch`` in ``docids``, resolves the
        salary rules used, builds one formatted row per payslip
        (ordered by id) with per-rule amounts, and accumulates
        per-rule and grand totals across the batch.

        :param docids: ids of ``hr.payslip_batch`` records to render
        :param data: unused, present for the ``_get_report_values``
            override signature required by the QWeb report engine
        :return: dict with ``doc_ids``, ``doc_model`` and ``docs`` —
            the list of per-batch context dicts (``batch``, ``rules``,
            ``payslips``, ``rule_totals``, ``rule_totals_fmt``,
            ``grand_total``, ``grand_total_fmt``) consumed by the
            report template
        """
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
