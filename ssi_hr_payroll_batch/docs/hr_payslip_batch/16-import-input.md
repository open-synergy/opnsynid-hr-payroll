# Import Payslip Input of Employee Payslip Batch

> **Module:** ssi_hr_payroll_batch\
> **Model:** `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Data:** An xlsx file previously downloaded via **Export Input** (see
  `15-export-input.md`), with amounts filled in for the desired input codes, and its
  header row left untouched.
- **Access:** User is in group `Payslip Batch / User` (required to open and act on the
  batch where this button appears; the button itself is not guarded by a dedicated
  policy field).

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to import payslip inputs into (status **In Progress**).
3. On the **Payslips** tab, click the **Import Input** button.
4. In the wizard that appears, click the file field and select the edited xlsx file.
5. Click **Import**.

## Post-Condition

- On success, the wizard closes and, for every row whose Payslip ID belongs to a
  **Draft** payslip of this batch, the amount of each recognized input code column is
  written onto that payslip's matching **Input Lines**. Rows with a blank or non-numeric
  Payslip ID are silently skipped.
- If any row's Payslip ID does not belong to this batch, or belongs to a payslip that is
  no longer in **Draft** status, or the header contains an input code that does not
  exist, the import fails as a whole with an error message — no input amounts are
  written.
- Uploading the file itself is not covered by this document; only the click-flow around
  it is.
