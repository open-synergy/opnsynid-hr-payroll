# Create Salary Rule Category

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule_category`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rule Categories\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule Category`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Rule Categories** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the salary rule category name.
   - **Code**: Enter a unique code for this category.
   - **Parent**: _(Optional)_ Select another salary rule category as the parent of this
     record. Leave it empty to create a top-level category. This field builds the
     category hierarchy.
   - **Active**: Enabled by default. Keep it enabled so the category can be selected on
     salary rules.
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Review the **Childs** tab. It lists the categories whose **Parent** is
   this record (field **Children**). The list is normally filled automatically when
   another category selects this record as its **Parent**, so it does not need to be
   filled in manually here.
6. _(Optional)_ Write additional information in the **Note** tab.
7. Click **Save**.

## Post-Condition

- A new Salary Rule Category record is created.
- The new record can be selected on the **Category** field of a Salary Rule. This is why
  the category has to be created first — a Salary Rule cannot be saved without one.
