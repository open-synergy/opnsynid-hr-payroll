# Create Salary Structure

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_structure`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Structures\
> **Actor:** user in group `Human Resource - Configurator / Salary Structure`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one Salary Rule already exists, if the **Rules** tab is going to be
  filled in right away. A salary structure without any salary rule can still be saved,
  because the **Salary Rules** field is not mandatory.
- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Structures** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the header fields:
   - **Name**: Enter the salary structure name.
   - **Code**: Enter a unique code for this salary structure.
   - **Parent**: _(Optional)_ Select another salary structure as the parent of this
     record. Leave it empty to create a top-level structure. The salary rules of the
     parent structure also apply to this structure.
   - **Active**: Enabled by default. Keep it enabled so the salary structure can be
     selected on a payslip.
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Fill in the **Rules** tab:
   - **Salary Rules**: Select the salary rules that apply to this structure. Selecting a
     salary rule here does not remove it from any other salary structure — the same
     salary rule can be used by several structures at once.
6. _(Optional)_ Write additional information in the **Note** tab.
7. Click **Save**.

## Post-Condition

- A new Salary Structure record is created.
- The new record can be selected when preparing a payslip.
