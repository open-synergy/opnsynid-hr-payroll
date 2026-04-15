# Approve Employee Payslip

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** and an accounting
  journal entry is automatically created.
- If there are still pending approval levels, status remains **Waiting for Approval**.
