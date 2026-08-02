.. |badge1| image:: https://img.shields.io/badge/maturity-Alpha-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alpha
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2|

=================================================
Employee Payslip Batch - Salary Summary Report
=================================================

Adds a salary summary report for Employee Payslip Batch.

The report shows all payslips in a batch as rows and salary rules as dynamic
columns, ordered by salary rule sequence. Features:

* On-screen HTML view with links to individual payslip forms
* Export to XLSX (Excel) with hyperlinks to payslip forms
* Print/download as PDF (landscape orientation)
* Dynamic columns — automatically adapts to whichever salary rules exist in the batch
* Grand totals per salary rule column

Work Instruction
================

* `Print Salary Summary Report of Employee Payslip Batch <docs/hr_payslip_batch/20-salary-summary-report.html>`_

**Table of contents**

.. contents::
   :local:

Usage
=====

1. Open a **Payslip Batch** record (state must not be Draft).
2. Click **Salary Summary** to view the report on-screen in the browser.
3. Click **Export XLSX** to download the Excel file.
4. Alternatively, use the **Print** menu (top-right) to choose HTML / PDF / XLSX.

From the HTML on-screen view:

* Click any employee name to open the corresponding payslip form.
* Use the **Export XLSX** or **Download PDF** buttons at the top of the report.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/open-synergy/opnsynid-hr-payroll/issues>`_.

Credits
=======

Authors
~~~~~~~

* OpenSynergy Indonesia
* PT. Simetri Sinergi Indonesia
