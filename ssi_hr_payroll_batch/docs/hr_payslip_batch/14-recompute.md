# Re-Compute Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Access:** User is in group `Payslip Batch / User` (required to open and act on the
  batch where this button appears; the button itself is not guarded by a dedicated
  policy field).

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to recompute (status **In Progress**).
3. On the **Payslips** tab, click the **Re-Compute** button.

## Post-Condition

- Every payslip on the **Payslips** tab that was in **Draft** status has its salary
  rules recomputed, refreshing its payslip lines.
- Payslips that are no longer **Draft** are left untouched.
- The batch itself is not moved to a different status.
