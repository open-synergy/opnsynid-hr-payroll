# Restart Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip / Validator` (module `ssi_hr_payroll`)\
> **State:** `cancel`/`reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for those
  states to group `Payslip / Validator` (module `ssi_hr_payroll`).
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- All cancelled or rejected payslips in the batch are automatically restarted to
  **Draft**.
- Status returns to **Draft**.
