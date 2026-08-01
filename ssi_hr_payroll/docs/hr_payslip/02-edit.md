# Edit Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** user in group `Payslip / User`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_payslip` (Compute Payslip), `action_reload_input_lines`
> (Reload), `action_recompute_allowance_ref` (Reload), `action_recompute_deduction_ref` (Reload)

## Pre-Condition

- **Record:** Status is **Draft**.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Find and open the payslip record to edit.
3. Change the required fields.
4. _(Optional)_ On the **Input Lines** tab, click **Reload** to rebuild the **Input
   Lines** list from the salary rules of the current **Salary Structure**, discarding
   any input lines currently on the tab (including manually added lines or edited
   amounts). This is the only way to bring the input lines back in sync with the
   structure once they have been changed by hand, or after the structure's rules changed
   — there is no other button or field that does this. Skipping this step leaves the
   input lines exactly as they are, and **Compute Payslip** (step 6) will evaluate the
   salary rules against whatever input line values are currently on the tab.
5. _(Optional)_ On the **Reference** tab:
   - Click **Reload** under _Allowance_ to search again for unreconciled allowance
     journal entries within the payslip period and refresh **Allowance Ref Move Lines**
     with the result. There is no manual way to add these lines — they can only be
     populated by this button. Skipping this step keeps the allowance reference lines as
     they currently are, so entries created or reconciled after the payslip was last
     computed will not be picked up.
   - Click **Reload** under _Deduction_ to search again for unreconciled deduction
     journal entries within the payslip period and refresh **Deduction Ref Move Lines**
     with the result. There is no manual way to add these lines — they can only be
     populated by this button. Skipping this step keeps the deduction reference lines as
     they currently are, so entries created or reconciled after the payslip was last
     computed will not be picked up.
6. _(Optional)_ Click **Compute Payslip** and confirm the dialog to refresh the payslip.
   This automatically re-runs both **Reload** actions on the **Reference** tab (step 5),
   then re-evaluates every applicable salary rule against the current **Input Lines**
   and rebuilds the **Details** tab from the result. There is no other way to refresh
   **Details** after changing **Salary Structure**, **Input Lines**, or the reference
   move lines — it can only be updated by this button. Skipping this step leaves
   **Details** showing payslip lines that no longer match the record's current values.
7. Click **Save**.

## Post-Condition

- The payslip record is updated with the new values.
- If **Compute Payslip** was used, the **Details** tab reflects the recomputed payslip
  lines.
