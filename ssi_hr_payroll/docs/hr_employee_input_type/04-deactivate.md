# Deactivate Employee Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.employee_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Employee Input Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Input Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Employee Input Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated employee input types cannot be selected on new employee input lines.
- Employee input lines that already use this employee input type are not affected.
