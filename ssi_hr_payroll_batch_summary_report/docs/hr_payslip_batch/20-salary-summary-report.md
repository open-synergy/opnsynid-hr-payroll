# Print Salary Summary Report of Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch_summary_report\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `07-start`\
> **Extends:** ssi_hr_payroll_batch — model `hr_payslip_batch`, new action buttons

This module adds two report buttons to the payslip batch form header: **Salary Summary**
(`action_print_salary_summary`, an on-screen/PDF report) and **Export XLSX**
(`action_export_salary_summary_xlsx`, an XLSX export).

## Pre-Condition

- **Module:** `ssi_hr_payroll_batch_summary_report` is installed.
- **Record:** Status is **not Draft** (i.e. it has left Draft — for example after it has
  been Started/opened). While the batch is in Draft both report buttons are hidden; they
  appear only once the batch is no longer in Draft.
- **Record:** The batch already has payslips, so the summary has data to render.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to report.
3. Click the **Salary Summary** button to view/print the salary summary report. The UI
   test only verifies that the button is displayed and enabled; the rendered report
   itself is outside the scope of the tour.
4. Click the **Export XLSX** button to download the salary summary as an XLSX file. The
   UI test only verifies that the button is displayed and enabled; the downloaded file
   itself is outside the scope of the tour.
5. Return to the **Payslip Batches** list.
6. Open a batch that is still in **Draft**.
7. Observe that neither the **Salary Summary** nor the **Export XLSX** button is
   displayed.

## Post-Condition

- The **Salary Summary** report opens for the batch.
- The **Export XLSX** file is downloaded for the batch.
- Neither the **Salary Summary** nor the **Export XLSX** button is displayed on a batch
  that is still in Draft.
