# Create Salary Contribution

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_contribution`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Contributions\
> **Actor:** user in group `Human Resource - Configurator / Salary Contribution`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** The receiving partner already exists in the Contact master data, if the
  **Partner** field is going to be filled in.
- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Contributions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the salary contribution name.
   - **Code**: Enter a unique code for this salary contribution.
   - **Partner**: _(Optional)_ Select the party that receives the contribution, for
     example the insurance or social security institution. It can be left empty and
     filled in later.
   - **Active**: Enabled by default. Keep it enabled so the salary contribution can be
     selected on salary rules.
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Write additional information in the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Salary Contribution record is created.
- The new record can be selected on the **Salary Contribution** field in the **General**
  tab of a Salary Rule.
