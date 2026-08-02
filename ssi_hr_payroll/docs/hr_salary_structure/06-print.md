# Print Salary Structure

> **Module:** ssi_hr_payroll\
> **Model:** `hr.salary_structure`\
> **Menu:** Human Resource > Configuration > Payroll > Salary Structures\
> **Actor:** user in group `Human Resource - Configurator / Salary Structure`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The salary structure record to print already exists.
- **Config:** At least one `print_document_type` is configured for the
  `hr.salary_structure` model with a report linked to it. Without this, the wizard still
  opens but offers no report to select — a silent dead end rather than an error.

## Flow

1. Open the **Human Resource > Configuration > Payroll > Salary Structures** menu.
2. Open the salary structure record to print.
3. Click the **Print** button.
4. In the **Select Report To Print** wizard, select the report under **Type** and
   **Report Template**.
5. Click the **Print** button on the wizard.

## Post-Condition

- The selected report is generated and downloaded to the user's device.
