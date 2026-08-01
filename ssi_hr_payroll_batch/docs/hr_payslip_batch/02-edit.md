# Edit Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_reload_employee` (Reload)

## Pre-Condition

- **Record:** Status is **Draft**.

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. _(Optional)_ On the **Employees** tab, click **Reload** to replace **Employees** with
   every employee who currently has a salary structure assigned and matches the type's
   employee filter (see **Allowed Employees**), discarding any employees added or
   removed by hand on the tab. There is no other way to bring the list back in sync with
   the filter once it has been edited manually — Reload is the only button that does
   this. Skipping this step leaves **Employees** exactly as it is; **Start**
   (`07-start`) will fail with "No employees selected" if the tab ends up empty.
5. Click **Save**.

## Post-Condition

- The Payslip Batch record is updated with the new values.
- If **Reload** was used, the **Employees** tab reflects the employees currently allowed
  by the type's filter.
