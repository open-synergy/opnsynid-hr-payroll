# Deactivate Salary Rule Category

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule_category`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rule Categories\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule Category`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Rule Categories** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated categories cannot be selected on new salary rules or as the **Parent** of
  another category.
- Salary rules that already use this category are not affected.
