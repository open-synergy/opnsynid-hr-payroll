# Create Employee Payslip

> **Module:** ssi_hr_payroll_documenso_signing
>
> **Extends:** ssi_hr_payroll — model `hr.payslip`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_payroll_documenso_signing` is installed.

## Modified Flow

- Anchor: on the base Flow step 2 (after clicking **New** / **Create** the payslip form
  opens in edit mode), the notebook gains an additional tab **Signature Requests** — the
  Documenso Signing page contributed by this module.
- The tab is present from the moment the form renders (it does not require the record to
  be saved, confirmed, or approved first). It groups the Documenso e-signing surface for
  the payslip:
  - an **Approval Signature Request** field, showing the signature request that drives
    approval once the active approval template uses a Documenso signing template;
  - a **New Signing Request** button and an **Open Signature Requests** button;
  - the list of signature requests linked to this payslip.

## Post-Condition

- Unchanged from base. Additionally, the **Signature Requests** tab is available on the
  payslip form for managing Documenso e-signing on the record.
