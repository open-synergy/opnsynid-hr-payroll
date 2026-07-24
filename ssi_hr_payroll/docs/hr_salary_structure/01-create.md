# Create Salary Structure

## Pre-Condition

- At least one Salary Rule already exists, if the **Rules** tab is going to be filled in
  right away. A salary structure without any salary rule can still be saved, because the
  **Salary Rules** field is not mandatory.

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
4. _(Optional)_ Fill in the **Rules** tab:
   - **Salary Rules**: Select the salary rules that apply to this structure. Selecting a
     salary rule here does not remove it from any other salary structure — the same
     salary rule can be used by several structures at once.
5. _(Optional)_ Write additional information in the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Salary Structure record is created.
- The new record can be selected when preparing a payslip.
