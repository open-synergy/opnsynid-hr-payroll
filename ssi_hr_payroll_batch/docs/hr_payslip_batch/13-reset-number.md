# Reset Document Number — Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip / Validator` (module `ssi_hr_payroll`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done** status,
  according to the sequence template configuration.
