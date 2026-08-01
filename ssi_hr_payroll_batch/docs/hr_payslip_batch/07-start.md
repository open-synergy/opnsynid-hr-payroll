# Open Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **State:** `draft` → `open`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** At least one employee is selected on the **Employees** tab.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `draft` to group `Payslip Batch / User`.
- **Access:** User has _Can Open_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **In Progress**.
- A payslip record is automatically created for each selected employee, with the period
  dates, batch date, type, and accounting configuration inherited from the batch.
- Payslips appear on the **Payslips** tab.

## Related Views

- The **Payslip** smart button (`action_open_payslip`) on the button box opens the list
  of payslips generated for this batch, filtered by `batch_id`. It only navigates to a
  dedicated list/form view of those payslips — it does not write any field or change
  state, so it has no work instruction or tour of its own.
