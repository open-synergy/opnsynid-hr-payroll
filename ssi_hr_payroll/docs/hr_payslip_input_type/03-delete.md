# Delete Payslip Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Input Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Input Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Data:** The record is not referenced by any payslip input line.
- **Data:** The record is not referenced by any salary rule.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Input Types** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- If a record is still referenced by a payslip input line or by a salary rule, the
  deletion is rejected and an error message appears. Deactivate the record instead.
