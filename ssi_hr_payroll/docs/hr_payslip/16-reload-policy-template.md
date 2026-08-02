# Reload Policy Template of Employee Payslip

> **Module:** ssi_hr_payroll\
> **Model:** `hr.payslip`\
> **Menu:** Human Resource > Payroll > Payslips\
> **Actor:** administrator — user in group `Administration / Settings` (`base.group_system`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** An existing payslip is open, in any status.
- **Config:** An active `policy.template` for `hr.payslip` is configured. If no template
  matches this record, clicking the button still succeeds but leaves **Policy Template**
  empty — a silent failure the actor should watch for.
- **Access:** User is a member of group `Administration / Settings`
  (`base.group_system`); without it, the **Reload Template Policy** button on the
  **Policies** tab is not rendered at all.

## Flow

1. Open the **Human Resource > Payroll > Payslips** menu.
2. Open the payslip whose policy template needs to be reloaded.
3. Open the **Policies** tab.
4. Click the **Reload Template Policy** button.

## Post-Condition

- The **Policy Template** field is reloaded with the template that currently matches the
  record.
- The policy fields below it (**Can Restart**, **Can Input Manual Document Number**)
  recompute from the reloaded template.
