# Restart Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / Validator`\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to group `Payslip / Validator`.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
