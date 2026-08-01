# Delete Employee Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.employee_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Employee Input Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Input Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Data:** The record is not referenced by any employee input line.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Employee Input Types** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- If a record is still referenced by an employee input line, the deletion is rejected
  and an error message appears. Deactivate the record instead.
