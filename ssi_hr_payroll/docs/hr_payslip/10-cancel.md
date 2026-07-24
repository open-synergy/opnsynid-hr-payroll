# Cancel Employee Payslip

## Pre-Condition

- Record is in a status that allows cancellation (usually **Draft**, **Waiting for
  Approval**, or **Done**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the payslip was in **Done** status, the associated accounting journal entry is
  reversed and deleted automatically.
