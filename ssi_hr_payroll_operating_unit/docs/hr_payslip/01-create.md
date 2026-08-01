# Create Employee Payslip

> **Module:** ssi_hr_payroll_operating_unit
>
> **Extends:** ssi_hr_payroll — model `hr.payslip`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_payroll_operating_unit` is installed.

## Additional Fields

When this module is installed, the create form gains one field, shown only to users in
the **Operating Unit / Multiple Operating Units** group
(`operating_unit.group_multi_operating_unit`):

- **Operating Unit**: The operating unit the payslip belongs to. Displayed after the
  **Company** field. When the payslip is posted, this operating unit is propagated to
  the generated accounting entry. Defaults to the user's default operating unit.

## Modified — Record Visibility

- The Payslips list is filtered by operating unit (record rule). A user only sees
  payslips of the operating units they are assigned to. This is not a Flow step.
