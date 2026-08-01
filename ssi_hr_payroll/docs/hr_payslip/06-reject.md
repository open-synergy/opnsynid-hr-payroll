# Reject Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** approver on the approval level that is currently pending (group `Payslip / Validator`)\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `reject_ok` to the
  approver on the pending level.
- **Access:** User is registered as an approver on the active approval template.
- **Access:** User has _Can Reject_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
