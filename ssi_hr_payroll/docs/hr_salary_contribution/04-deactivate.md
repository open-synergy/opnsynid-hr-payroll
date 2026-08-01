# Deactivate Salary Contribution

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_contribution`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Contributions\
> **Actor:** user in group `Human Resource - Configurator / Salary Contribution`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Contributions** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated salary contributions cannot be selected on new salary rules.
- Salary rules that already use this record are not affected.
