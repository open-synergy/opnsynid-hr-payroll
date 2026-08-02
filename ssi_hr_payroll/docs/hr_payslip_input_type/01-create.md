# Create Payslip Input Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_input_type`\
> **Menu:** Human Resource > Configuration > Payroll > Input Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Input Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Input Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the payslip input type name.
   - **Code**: Enter a unique code for this input type.
   - **Active**: Enabled by default. Keep it enabled so the input type can be selected
     on payslip input lines and salary rules.
   - **Default Amount**: _(Optional)_ Enter the amount that automatically fills the
     **Amount** field when this input type is selected on a payslip input line. The
     default value is `0.0` and it may be left as is when the amount always differs per
     payslip.
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Write additional information in the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Payslip Input Type record is created.
- The new record can be selected on the **Input Type** field of a payslip input line and
  on the **Input Types** tab of a Salary Rule.
