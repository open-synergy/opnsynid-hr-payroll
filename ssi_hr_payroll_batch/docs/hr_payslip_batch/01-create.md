# Create Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_reload_employee` (Reload)

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type**: Select the payslip type. **Accounting Method** and **Journal** are
     automatically filled from the selected type. Change if needed.
   - **Date**: Select the batch date (accounting date).
   - **Date Start** / **Date End**: Select the payroll period start and end dates.
4. _(Optional)_ Adjust accounting configuration fields if different from the type
   defaults:
   - **Accounting Method**: _Journal at Payslip_ or _Journal at Batch_.
   - **Journal**: Required when Accounting Method is _Journal at Batch_.
   - **Analytic Account**, **Debit Usage**, **Credit Usage**.
5. On the **Employees** tab, select the employees to include in this batch. Use the
   **Reload** button to automatically populate employees who have a salary structure
   assigned.
6. Click **Save**.

## Post-Condition

- A new Payslip Batch record is created in **Draft** status.
- No payslips are generated yet; they are created when the batch is opened.
