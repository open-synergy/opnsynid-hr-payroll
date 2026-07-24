# Create Employee Payslip

> **Module:** ssi_hr_payroll_work_log **Extends:** ssi_hr_payroll — model `hr_payslip`,
> aksi `01-create`

## Additional Fields

When this module is installed, the payslip form gains a **Work Log** tab used to plan
and review the work performed for the payslip:

- **Estimation** (`work_estimation`): The estimated work amount for the payslip. Entered
  manually.
- **Work Log Analytic Account** (`work_log_analytic_account_id`): The analytic account
  used for the payslip's work logs. Selected manually.
- **Work Logs** (`work_log_ids`): The list of work log lines linked to this payslip.
- **Total** / **Remaining** / **Excess** (`total_work` / `remaining_work` /
  `excess_work`): Read-only totals computed from the work logs against the estimation.

The **Work Log** tab is appended to the payslip form by the work object mixin; no view
customization is defined in this module.
