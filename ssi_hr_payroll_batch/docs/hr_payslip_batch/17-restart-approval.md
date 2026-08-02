# Restart Approval Process Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip / Validator` (module `ssi_hr_payroll`)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**, and the batch currently has no
  approval template assigned, so the approval process is stalled without an approver.
- **Config:** An active `policy.template` for this model grants `restart_approval_ok`
  for state `confirm` to group `Payslip / Validator` (module `ssi_hr_payroll`) when the
  record has no approval template assigned.
- **Config:** An active `approval.template` for this model matches this record, with an
  approver group configured for its approval level, so the process can be rebuilt once
  restarted.
- **Access:** User has _Can Restart Approval Process_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch whose approval process is stalled.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- The **Approvals** tab displays the approval list newly formed from the approval
  template.
