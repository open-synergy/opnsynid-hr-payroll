# Create Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch_work_log\
> **Extends:** ssi_hr_payroll_batch — model `hr_payslip_batch`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_payroll_batch_work_log` is installed.

## Additional Fields

When this module is installed, the payslip batch form gains a **Work Log** tab used to
plan and review the work performed for the batch:

- **Work Estimation** (`work_estimation`): The estimated work amount for the batch.
  Entered manually.
- **Work Log Analytic Account** (`work_log_analytic_account_id`): The analytic account
  used for the batch's work logs. Selected manually.
- **Work Logs** (`work_log_ids`): The list of work log lines linked to this batch.
- **Total Work** / **Remaining Work** / **Excess Work** (`total_work` / `remaining_work`
  / `excess_work`): Read-only totals computed from the work logs against the estimation.

The **Work Log** tab is appended to the payslip batch form by the work object mixin; no
view customization is defined in this module.
