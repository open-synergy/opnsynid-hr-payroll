# Create Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / User`\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_compute_payslip` (Compute Payslip), `action_reload_input_lines`
> (Reload), `action_recompute_allowance_ref` (Reload), `action_recompute_deduction_ref` (Reload)

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee**: Select the employee. **Department**, **Manager**, and **Job
     Position** are automatically filled from the selected employee.
   - **Date Start**: Select the payroll period start date.
   - **Date End**: Select the payroll period end date.
   - **Date**: Select the accounting date.
   - **Type**: Select the payslip type. **Journal** is automatically filled from the
     selected type. Change if needed.
   - **Salary Structure**: Automatically filled from the employee's default salary
     structure. Change if needed. Input lines on the _Input Lines_ tab are automatically
     populated when the salary structure is selected.
4. _(Optional)_ On the **Input Lines** tab, review and adjust input line values as
   needed. Use the **Reload** button to re-populate input lines from the selected salary
   structure.
5. _(Optional)_ On the **Reference** tab:
   - Click **Reload** under _Allowance_ to load reference allowance journal entries
     within the period.
   - Click **Reload** under _Deduction_ to load reference deduction journal entries
     within the period.
6. Click **Compute Payslip** and confirm the dialog to compute the payslip lines.
7. Click **Save**.

## Post-Condition

- A new payslip record is created in **Draft** status.
- Payslip lines are computed and displayed on the **Details** tab.
