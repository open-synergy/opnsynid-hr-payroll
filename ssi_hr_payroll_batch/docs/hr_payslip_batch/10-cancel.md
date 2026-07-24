# Cancel Employee Payslip Batch

## Pre-Condition

- Record is in a status that allows cancellation (**Draft**, **In Progress**, **Waiting
  for Approval**, or **Done**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- All payslips in the batch that are not yet cancelled are automatically cancelled.
- Status changes to **Cancelled**.
- If the batch was in **Done** status and **Accounting Method** was _Journal at Batch_,
  the batch-level journal entry is reversed and deleted automatically.
