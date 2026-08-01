# Export Payslip Input of Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is not **Draft** (the button is hidden while the batch is Draft; at
  least the batch's payslips must already exist).
- **Access:** User is in group `Payslip Batch / User` (required to open and act on the
  batch where this button appears; the button itself is not guarded by a dedicated
  policy field).

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to export payslip inputs from (any status other than **Draft**).
3. On the **Payslips** tab, click the **Export Input** button.
4. The browser downloads an xlsx spreadsheet named `payslip_batch_input_<number>.xlsx`
   (or `payslip_batch_input_<database id>.xlsx` when the batch has no document number
   yet). It has one row per payslip, with the payslip's database ID, employee name, and
   one column per input code used by the batch's payslips, filled with each payslip's
   current input amount for that code.

## Post-Condition

- An xlsx spreadsheet listing every payslip's input amounts is downloaded to the user's
  browser.
- The spreadsheet is also stored as an attachment on the batch record.
- The batch and its payslips are not modified; the batch's status is unchanged.
