# Approve Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** approver on the approval level that is currently pending (group `Payslip / Validator`)\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `approve_ok` to the
  approver on the pending level.
- **Access:** User is registered as an approver on the active approval template.
- **Access:** User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** and an accounting
  journal entry is automatically created.
- If there are still pending approval levels, status remains **Waiting for Approval**.
