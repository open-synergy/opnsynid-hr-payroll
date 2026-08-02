# Create Payslip Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_type`\
> **Menu:** Human Resource > Configuration > Payroll > Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model.

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
4. _(Optional)_ Click **Generate Code** in the header to have the system assign a code
   from the configured sequence template automatically. It only replaces a **Code**
   value that is still `/`; if you already typed your own code in the previous step,
   skip this step — the button leaves any other value untouched.
5. _(Optional)_ Fill in the accounting configuration fields:
   - **Journal**: Select the default accounting journal for payslip entries of this
     type. If set, it is automatically propagated to new payslips and batches.
   - **Analytic Account**: Select the default analytic account for journal items.
   - **Debit Usage**: Select the product usage type used to resolve the debit account.
   - **Credit Usage**: Select the product usage type used to resolve the credit account.
6. _(Optional)_ Configure which analytic accounts, debit/credit usages, and employees
   are allowed on payslips of this type. Open one of the configurator tabs — **Analytic
   Account Configurator**, **Debit Usage Configurator**, **Credit Usage Configurator**,
   or **Employee Configurator** — and set:
   - **Selection Method**: how the allowed records are computed.
     - _Manual_: pick specific records in the field that appears below (e.g. **Analytic
       Accounts**, **Debit Usages**, **Credit Usages**, or **Employees**).
     - _Domain_ (default): enter a domain filter in the field that appears below (e.g.
       **Domain**). An empty domain (`[]`) allows every record — the type's behavior
       before this configurator existed.
     - _Python Code_: enter Python code in the field that appears below (e.g. **Python
       Code**) that returns the allowed records.
7. Click **Save**.

## Post-Condition

- A new Payslip Type record is created and available for selection on payslips and
  payslip batches.
- Payslips using this type only allow selecting an analytic account, debit usage, credit
  usage, or employee that passes the corresponding configurator.
