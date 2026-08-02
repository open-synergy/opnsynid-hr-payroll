# Print Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The batch exists (any status — the **Print** button is not guarded by any
  `states=`/`attrs` condition and stays available throughout the record's lifecycle).
- **Config:** At least one `print_document_type` is configured for the
  `hr.payslip_batch` model with a report linked to it. Without this, the wizard still
  opens but offers no report to select — a silent dead end rather than an error.
- **Access:** User is in group `Payslip Batch / User` (required to open and act on the
  batch where this button appears; the button itself is not guarded by a dedicated
  policy field).

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to print (any status).
3. Click the **Print** button in the header.
4. In the **Select Report To Print** wizard, select the report under **Type** and
   **Report Template**.
5. Click the **Print** button on the wizard.

## Post-Condition

- The selected report is generated and downloaded to the user's device.
- The batch and its payslips are not modified; the batch's status is unchanged.
