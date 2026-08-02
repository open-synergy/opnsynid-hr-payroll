# Create Employee Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.employee_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Employee Input Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Input Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model.

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
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Write additional information in the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Employee Input Type record is created.
- The new record can be selected on the **Input Type** field of an employee input line.
