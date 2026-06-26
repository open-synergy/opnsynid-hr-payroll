# Troubleshoot — Employee Payslip Batch

## Error: No Employees Selected

**Symptom:** An error appears when clicking the **Open** button.

**Cause:** The **Employees** tab has no employees selected.

**Solution:** Go to the **Employees** tab and add at least one employee before opening
the batch. Use the **Reload** button to automatically populate all employees who have a
salary structure assigned.

---

## Error: Journal Is Required When Accounting Method Is 'Journal at Batch'

**Symptom:** A validation error appears when saving or confirming the batch.

**Cause:** **Accounting Method** is set to _Journal at Batch_ but no **Journal** is
selected.

**Solution:** Select a journal in the **Journal** field, or change the **Accounting
Method** to _Journal at Payslip_.

---

## Error: Payslips Could Not Be Transitioned to Done

**Symptom:** An error appears during the **Approve** action, stating that one or more
payslips could not reach **Done** status.

**Cause:** One or more payslips in the batch have a configuration issue that prevents
them from being approved, such as:

- Missing approval template or approver configuration.
- Required fields (e.g., salary structure, journal) not set on the payslip.

**Solution:**

1. Open the **Payslips** tab on the batch.
2. Identify the payslip(s) that are not in **Done** status.
3. Open each affected payslip and resolve the configuration issue.
4. Return to the batch and retry the **Approve** action.

---

## Error: Journal Has No Default Account Configured

**Symptom:** An error appears when the batch transitions to **Done** status, related to
the batch balance adjustment entry.

**Cause:** The journal selected on the batch does not have a default account, which is
needed to post the balance adjustment journal line.

**Solution:** Go to **Accounting > Configuration > Journals**, open the relevant
journal, and set the **Default Account** field.
