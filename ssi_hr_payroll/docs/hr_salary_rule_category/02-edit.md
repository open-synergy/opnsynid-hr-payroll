# Edit Salary Rule Category

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule_category`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rule Categories\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule Category`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Rule Categories** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Save**.

## Post-Condition

- The Salary Rule Category record is updated with the new values.
- The system rejects a recursive hierarchy: if the selected **Parent** is the record
  itself or one of its own descendants, an error message appears and the change is not
  saved.
