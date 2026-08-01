# Delete Salary Contribution

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_contribution`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Contributions\
> **Actor:** user in group `Human Resource - Configurator / Salary Contribution`\
> **Requires:** `01-create`

## Pre-Condition

- **Data:** The record is not referenced by any salary rule.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Contributions** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- If a record is still referenced by a salary rule, the deletion is rejected and an
  error message appears. Deactivate the record instead.
