# Create Payslip Input Type

## Pre-Condition

- None.

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
4. _(Optional)_ Write additional information in the **Note** tab.
5. Click **Save**.

## Post-Condition

- A new Payslip Input Type record is created.
- The new record can be selected on the **Input Type** field of a payslip input line and
  on the **Input Types** tab of a Salary Rule.
