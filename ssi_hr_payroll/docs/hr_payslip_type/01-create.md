# Create Payslip Type

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the payslip type name.
   - **Code**: Enter a unique code for this type.
   - **Accounting Method**: Select how accounting entries are created.
     - _Journal at Payslip_ (default): each payslip creates its own journal entry.
     - _Journal at Batch_: the batch aggregates all payslip lines into a single journal
       entry.
4. _(Optional)_ Fill in the accounting configuration fields:
   - **Journal**: Select the default accounting journal for payslip entries of this
     type. If set, it is automatically propagated to new payslips and batches.
   - **Analytic Account**: Select the default analytic account for journal items.
   - **Debit Usage**: Select the product usage type used to resolve the debit account.
   - **Credit Usage**: Select the product usage type used to resolve the credit account.
5. Click **Save**.

## Post-Condition

- A new Payslip Type record is created and available for selection on payslips and
  payslip batches.
