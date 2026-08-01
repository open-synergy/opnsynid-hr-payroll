# Edit Salary Rule

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rules\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Rules** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Save**.

## Post-Condition

- The Salary Rule record is updated with the new values.
- The system rejects a recursive hierarchy: if the selected **Parent** is the record
  itself or one of its own descendants, an error message appears and the change is not
  saved.
