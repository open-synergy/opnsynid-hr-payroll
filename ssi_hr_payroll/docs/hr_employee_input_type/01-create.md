# Create Employee Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.employee_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Employee Input Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Input Type`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Employee Input Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the employee input type name.
   - **Code**: Enter a unique code for this employee input type.
   - **Active**: Enabled by default. Keep it enabled so the employee input type can be
     selected on employee input lines.
   - **Default Amount**: _(Optional)_ Enter the amount that automatically fills the
     **Amount** field when this employee input type is selected on an employee input
     line. The default value is `0.0` and it may be left as is when the amount always
     differs per employee.
4. _(Optional)_ Write additional information in the **Note** tab.
5. Click **Save**.

## Post-Condition

- A new Employee Input Type record is created.
- The new record can be selected on the **Input Type** field of an employee input line.
