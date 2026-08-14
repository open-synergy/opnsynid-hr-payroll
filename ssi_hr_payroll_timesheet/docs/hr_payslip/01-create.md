# Create Employee Payslip

> **Module:** ssi_hr_payroll_timesheet
>
> **Extends:** ssi_hr_payroll — model `hr.payslip`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_payroll_timesheet` is installed.
- **Data:** At least one timesheet (`hr.timesheet`) exists for the same employee, is in
  the **Done** state, and its period falls inside the payslip period. Without such a
  timesheet the **Timesheet** tab is shown but stays empty.

## Additional Fields

When this module is installed, the payslip form gains a **Timesheet** tab, placed after
the **Input Lines** tab:

- **Timesheet Computations** (`timesheet_computation_ids`): The computation lines taken
  from the employee's done timesheets that fall inside the payslip period. Read-only.

The tab lists each computation line in four columns:

- **Timesheet** (`sheet_id`, shown in the column header as **# Sheet**): The timesheet
  the computation line comes from.
- **Code** (`code`): The code of the computation item.
- **Item** (`item_id`): The computation item that produced the line.
- **Amount** (`amount`): The computed amount of the line.

This field is computed, not an input. The user does not fill it in and cannot add, edit,
or remove rows in the tab. Its value is recomputed from the employee's timesheets
whenever **Employee** (`employee_id`), **Date Start** (`date_start`), or **Date End**
(`date_end`) changes.
