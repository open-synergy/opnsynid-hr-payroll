# Delete Salary Structure

## Pre-Condition

- The record is not used by any payslip.
- The record has no child salary structure (no other salary structure selects this
  record as its **Parent**).

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Structures** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- If a record is still used by a payslip or still has a child salary structure, the
  deletion is rejected and an error message appears. Deactivate the record instead.
