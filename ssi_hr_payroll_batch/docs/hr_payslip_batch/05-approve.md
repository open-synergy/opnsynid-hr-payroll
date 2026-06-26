# Approve Employee Payslip Batch

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled:
  - All payslips in the batch are automatically transitioned to **Done**.
  - If **Accounting Method** is _Journal at Payslip_: each payslip creates its own
    accounting journal entry.
  - If **Accounting Method** is _Journal at Batch_: a single aggregated journal entry is
    created at the batch level, covering all payslip lines grouped by salary rule and
    partner.
  - Status changes to **Done**.
- If there are still pending approval levels, status remains **Waiting for Approval**.
