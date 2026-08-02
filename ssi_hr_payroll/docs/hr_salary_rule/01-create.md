# Create Salary Rule

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_rule`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Rules\
> **Actor:** user in group `Human Resource - Configurator / Salary Rule`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** At least one Salary Rule Category already exists. The **Category** field is
  mandatory, so a salary rule cannot be saved without it.
- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Rules** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the header fields:
   - **Name**: Enter the salary rule name.
   - **Code**: Enter a unique code for this salary rule. The code is the reference used
     by other salary rules when they read the result of this rule.
   - **Sequence**: Determines the calculation order of the salary rule — the smaller the
     number, the earlier the rule is computed. Filled with `5` by default. Change if
     needed.
   - **Active**: Enabled by default. Keep it enabled so the salary rule can be selected
     on a salary structure.
   - **Parent**: _(Optional)_ Select another salary rule as the parent of this record.
     Leave it empty to create a top-level rule. This field builds the salary rule
     hierarchy.
   - **Category**: _(Mandatory)_ Select the salary rule category this rule belongs to.
     The record cannot be saved while this field is empty.
   - **Product**: _(Optional)_ Select the product associated with this salary rule.
   - **Appear on Payslip**: _(Optional)_ Enable it so the line produced by this rule is
     shown on the payslip.
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. Fill in the **General** tab:
   - **Python Condition**: Python expression that decides whether this salary rule is
     applied. It is already filled with a default expression whose comments list the
     variables available for the evaluation. Adjust the expression as needed.
   - **Computation**: Python expression that produces the amount of this salary rule. It
     is already filled with a default expression whose comments list the variables
     available for the evaluation. Adjust the expression as needed.
   - **Salary Contribution**: _(Optional)_ Select the salary contribution record linked
     to this salary rule.
6. _(Optional)_ Fill in the **Accounting** tab. These fields are used when the payslip
   creates its accounting entry:
   - **Debit Account**: Select the account to be debited by this salary rule.
   - **Reconcile Debit Account**: Select the account used to reconcile the debit side.
   - **Reconcile Debit Move**: Enable it so the debit move line is marked to be
     reconciled.
   - **Credit Account**: Select the account to be credited by this salary rule.
   - **Reconcile Credit Account**: Select the account used to reconcile the credit side.
   - **Reconcile Credit Move**: Enable it so the credit move line is marked to be
     reconciled.
7. _(Optional)_ Fill in the **Input Types** tab. Repeat the following step as many times
   as needed:
   - Click **Add a line**, then select the payslip input type used by this salary rule.
8. _(Optional)_ Review the **Children** tab. It lists the salary rules whose **Parent**
   is this record (field **Child Salary Rule**). The list is normally filled
   automatically when another salary rule selects this record as its **Parent**, so it
   does not need to be filled in manually here.
9. _(Optional)_ Write additional information in the **Note** tab.
10. Click **Save**.

## Post-Condition

- A new Salary Rule record is created.
- The new record can be selected on a salary structure and is evaluated when a payslip
  is computed, following the order defined by **Sequence**.
