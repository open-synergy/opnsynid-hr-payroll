# Activate Salary Structure

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_structure`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Structures\
> **Actor:** user in group `Human Resource - Configurator / Salary Structure`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Structures** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The salary structures can be selected on new payslips and as the **Parent** of another
  salary structure.
