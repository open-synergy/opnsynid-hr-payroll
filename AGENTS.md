# Agent Instructions — opnsynid-hr-payroll

This file is intended for **AI assistants** (GitHub Copilot, Claude, Cursor, ChatGPT,
and similar tools) working inside this repository.

This repository contains Odoo 14 modules for **HR Payroll** features (Employee Payslip,
Payslip Batch), developed following SSI standard patterns (PT. Simetri Sinergi Indonesia
/ OpenSynergy Indonesia).

---

## Modules in This Repository

| Module                          | Description                                      |
| ------------------------------- | ------------------------------------------------ |
| `ssi_hr_payroll`                | Employee payslip processing and accounting entry |
| `ssi_hr_payroll_batch`          | Employee payslip batch processing                |
| `ssi_hr_payroll_batch_work_log` | Work log integration for payslip batch           |
| `ssi_hr_payroll_timesheet`      | Timesheet integration for payslip                |
| `ssi_hr_payroll_work_log`       | Work log integration for payslip                 |

---

## User Guide (Work Instructions)

Each module has a `docs/` directory containing **Work Instructions (IK)** — step-by-step
operational documentation for using the feature from the user's perspective.

### How to Answer User Questions About Feature Usage

1. Identify the feature being asked about (payslip, payslip batch, etc.).
2. Find the relevant Work Instruction from the index below.
3. **Read that file** before answering — do not fabricate steps from assumptions.
4. If a relevant extension module is installed (marked _additive_ below), also read its
   Work Instruction and **merge** it with the base IK.
5. Answer based on the content of the Work Instruction.

### Work Instruction Location Pattern

```
<module_name>/docs/<model_name>/<number>-<action>.md
```

---

## Work Instruction Index

### `ssi_hr_payroll` — Model: `hr.salary_rule_category`

Menu: **Human Resource > Configuration > Payroll > Salary Rule Categories**

| File                                                           | Action                            |
| -------------------------------------------------------------- | --------------------------------- |
| `ssi_hr_payroll/docs/hr_salary_rule_category/01-create.md`     | Create a new salary rule category |
| `ssi_hr_payroll/docs/hr_salary_rule_category/02-edit.md`       | Edit a salary rule category       |
| `ssi_hr_payroll/docs/hr_salary_rule_category/03-delete.md`     | Delete a salary rule category     |
| `ssi_hr_payroll/docs/hr_salary_rule_category/04-deactivate.md` | Deactivate a salary rule category |
| `ssi_hr_payroll/docs/hr_salary_rule_category/05-activate.md`   | Activate a salary rule category   |

---

### `ssi_hr_payroll` — Model: `hr.salary_rule`

Menu: **Human Resource > Configuration > Payroll > Salary Rules**

| File                                                  | Action                   |
| ----------------------------------------------------- | ------------------------ |
| `ssi_hr_payroll/docs/hr_salary_rule/01-create.md`     | Create a new salary rule |
| `ssi_hr_payroll/docs/hr_salary_rule/02-edit.md`       | Edit a salary rule       |
| `ssi_hr_payroll/docs/hr_salary_rule/03-delete.md`     | Delete a salary rule     |
| `ssi_hr_payroll/docs/hr_salary_rule/04-deactivate.md` | Deactivate a salary rule |
| `ssi_hr_payroll/docs/hr_salary_rule/05-activate.md`   | Activate a salary rule   |

---

### `ssi_hr_payroll` — Model: `hr.payslip`

Menu: **Human Resource > Payroll > Payslips**

| File                                                | Action                |
| --------------------------------------------------- | --------------------- |
| `ssi_hr_payroll/docs/hr_payslip/01-create.md`       | Create a new payslip  |
| `ssi_hr_payroll/docs/hr_payslip/02-edit.md`         | Edit a payslip        |
| `ssi_hr_payroll/docs/hr_payslip/03-delete.md`       | Delete a payslip      |
| `ssi_hr_payroll/docs/hr_payslip/04-confirm.md`      | Confirm a payslip     |
| `ssi_hr_payroll/docs/hr_payslip/05-approve.md`      | Approve a payslip     |
| `ssi_hr_payroll/docs/hr_payslip/06-reject.md`       | Reject a payslip      |
| `ssi_hr_payroll/docs/hr_payslip/10-cancel.md`       | Cancel a payslip      |
| `ssi_hr_payroll/docs/hr_payslip/12-restart.md`      | Restart a payslip     |
| `ssi_hr_payroll/docs/hr_payslip/13-reset-number.md` | Reset document number |

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the guidelines in the `copilot-instruction` repository (attached as a
separate workspace folder when available).
