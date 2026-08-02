# Edit Payslip Type

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip_type`\
> **Menu:** Human Resource > Configuration > Payroll > Types\
> **Actor:** user in group `Human Resource - Configurator / Payslip Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)\
> **Requires:** `01-create`

## Pre-Condition

- **Config:** An active `sequence.template` exists for this model.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Types** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. _(Optional)_ If the **Code** field still shows `/`, click **Generate Code** in the
   header to assign a code from the configured sequence template automatically. It
   leaves any other value untouched, so skip this step if the record already has a code
   you want to keep.
5. Click **Save**.

## Post-Condition

- The Payslip Type record is updated with the new values.
