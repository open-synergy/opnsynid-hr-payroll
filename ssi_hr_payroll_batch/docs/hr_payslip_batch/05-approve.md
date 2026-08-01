# Approve Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** approver on the approval level that is currently pending (group `Payslip Batch / Validator`)\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `approve_ok` to the
  approver on the pending level.
- **Access:** User is registered as an approver on the active approval template.
- **Access:** User has _Can Approve_ access right.

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
