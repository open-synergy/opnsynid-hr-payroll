# Create Employee Payslip

> **Module:** ssi_hr_payroll_timesheet **Extends:** ssi_hr_payroll — model `hr_payslip`,
> action `01-create`

## Additional Fields

When this module is installed, the payslip form gains a **Timesheet** tab, shown right
after the **Input Lines** tab:

- **Timesheet Computations** (tab **Timesheet**): A read-only list of the timesheet
  computation lines that belong to the payslip's employee within the payroll period. It
  is recomputed automatically from the selected **Employee**, **Date Start**, and **Date
  End** — it is never typed in by the user. The tab lets the payroll operator review
  which timesheet computations feed into the payslip before confirming it.
