# Confirm Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **State:** `open` → `confirm`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Record:** All payslips in the batch have been computed (payslip lines are
  populated).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `open` to group `Payslip Batch / User`.
- **Config:** An active `approval.template` for this model matches this record, with an
  approver group configured for its approval level.
- **Access:** User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- All draft payslips in the batch are automatically confirmed.
- Status changes to **Waiting for Approval**.
