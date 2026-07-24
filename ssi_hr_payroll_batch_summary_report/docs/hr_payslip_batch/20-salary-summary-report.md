# Print Salary Summary Report of Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch_summary_report **Extends:** ssi_hr_payroll_batch —
> model `hr_payslip_batch`, new action buttons

This module adds two report buttons to the payslip batch form header: **Salary Summary**
(`action_print_salary_summary`, an on-screen/PDF report) and **Export XLSX**
(`action_export_salary_summary_xlsx`, an XLSX export).

## Pre-Condition

- Record is **not** in **Draft** status (i.e. it has left Draft — for example after it
  has been Started/opened). While the batch is in Draft both report buttons are hidden;
  they appear only once the batch is no longer in Draft.
- The batch already has payslips, so the summary has data to render.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to report.
3. Click the **Salary Summary** button to view/print the salary summary report.
4. Click the **Export XLSX** button to download the salary summary as an XLSX file.

## Post-Condition

- The **Salary Summary** report opens for the batch.
- The **Export XLSX** file is downloaded for the batch.
