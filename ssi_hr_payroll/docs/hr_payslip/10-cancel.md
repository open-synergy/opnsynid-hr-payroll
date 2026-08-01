# Cancel Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / Validator`\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status allows cancellation (**Draft**, **Waiting for Approval**, or
  **Done**).
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to group `Payslip / Validator`.
- **Access:** User has _Can Cancel_ access right.

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
