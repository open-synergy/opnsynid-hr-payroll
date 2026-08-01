# Create Salary Rule Category

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule_category`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rule Categories\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule Category`

## Pre-Condition

- None.

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
4. _(Optional)_ Review the **Childs** tab. It lists the categories whose **Parent** is
   this record (field **Children**). The list is normally filled automatically when
   another category selects this record as its **Parent**, so it does not need to be
   filled in manually here.
5. _(Optional)_ Write additional information in the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Salary Rule Category record is created.
- The new record can be selected on the **Category** field of a Salary Rule. This is why
  the category has to be created first — a Salary Rule cannot be saved without one.
