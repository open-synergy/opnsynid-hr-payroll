# Activate Payslip Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Input Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Input Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Input Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The input types can be selected again on payslip input lines and on the **Input
  Types** tab of a Salary Rule.
