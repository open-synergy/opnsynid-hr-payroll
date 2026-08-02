# Print Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / Viewer`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The payslip exists (any status — the **Print** button is not guarded by
  status and stays available throughout the record's lifecycle).
- **Config:** At least one `print_document_type` is configured for the `hr.payslip`
  model with a report linked to it. Without this, the wizard still opens but offers no
  report to select — a silent dead end rather than an error.
- **Access:** User has read access to the payslip record.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to print.
3. Click the **Print** button.
4. In the **Select Report To Print** wizard, select the report under **Type** and
   **Report Template**.
5. Click the **Print** button on the wizard.

## Post-Condition

- The selected report is generated and downloaded to the user's device.
