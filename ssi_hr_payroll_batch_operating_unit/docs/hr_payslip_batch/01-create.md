# Create Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch_operating_unit\
> **Extends:** ssi_hr_payroll_batch — model `hr_payslip_batch`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_payroll_batch_operating_unit` is installed.

## Additional Fields

When this module is installed and the user belongs to the **Multi Operating Unit** group
(`operating_unit.group_multi_operating_unit`), the create form gains one field:

- **Operating Unit**: The operating unit the payslip batch belongs to. Selected on the
  create form to scope the batch to a specific operating unit. When set, the employees
  offered by the **Reload** button on the Employees tab are limited to employees
  assigned to that operating unit, and the value is propagated to each generated payslip
  and to the batch-level journal entry. The field is hidden for users who are not in the
  Multi Operating Unit group.

## Modified — Record Visibility

- Payslip batches are filtered by operating unit through a record rule: a user only sees
  batches whose operating unit is among the operating units they are assigned to. This
  is a data/access effect, not a Flow step.
