# Deactivate Payslip Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Input Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Input Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Input Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated input types cannot be selected on new payslip input lines or on the
  **Input Types** tab of a Salary Rule.
- Payslip input lines and salary rules that already use this input type are not
  affected.
