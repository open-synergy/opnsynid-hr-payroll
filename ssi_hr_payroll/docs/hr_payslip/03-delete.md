# Delete Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
