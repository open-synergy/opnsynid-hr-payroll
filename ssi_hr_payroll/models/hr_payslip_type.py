# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

ACCOUNTING_METHOD = [
    ("payslip", "Journal at Payslip"),
    ("batch", "Journal at Batch"),
]

M2O_CONFIGURATOR_SELECTION_METHOD = [
    ("manual", "Manual"),
    ("domain", "Domain"),
    ("code", "Python Code"),
]


class HrPayslipType(models.Model):
    """
    Configures the accounting behaviour of a category of payslips.

    Decides where the journal entry for a payslip is created
    (``accounting_method``), which journal, analytic account and
    debit/credit product usage to use, and which analytic accounts,
    usages and employees are selectable, each resolved through the
    M2O configurator strategy fields (manual/domain/Python code).
    """

    _name = "hr.payslip_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Payslip Type"

    accounting_method = fields.Selection(
        string="Accounting Method",
        selection=ACCOUNTING_METHOD,
        default="payslip",
        required=True,
        help="Controls where the journal entry is created. "
        "'Journal at Payslip' (default): each payslip creates its own journal entry. "
        "'Journal at Batch': the batch aggregates all payslip lines into a single entry.",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        ondelete="restrict",
        help="Accounting journal used for payslip entries of this type.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        help="Analytic account used for journal items of payslip entries of this type.",
    )
    debit_usage_id = fields.Many2one(
        string="Debit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help="Product usage type used to resolve the debit account "
        "of payslip entries of this type.",
    )
    credit_usage_id = fields.Many2one(
        string="Credit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help="Product usage type used to resolve the credit account "
        "of payslip entries of this type.",
    )
    analytic_account_selection_method = fields.Selection(
        string="Analytic Account Selection Method",
        selection=M2O_CONFIGURATOR_SELECTION_METHOD,
        default="domain",
        required=True,
        help="Strategy used to compute the analytic accounts allowed on payslips "
        "of this type. 'Manual' uses 'Analytic Accounts', 'Domain' evaluates "
        "'Analytic Account Domain', 'Python Code' evaluates "
        "'Analytic Account Python Code'.",
    )
    analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        relation="rel_payslip_type_2_analytic_account",
        column1="type_id",
        column2="analytic_account_id",
        help="Analytic accounts allowed on payslips of this type when "
        "'Analytic Account Selection Method' is set to 'Manual'.",
    )
    analytic_account_domain = fields.Text(
        string="Analytic Account Domain",
        default="[]",
        help="Domain used to filter the analytic accounts allowed on payslips "
        "of this type when 'Analytic Account Selection Method' is set to "
        "'Domain'.",
    )
    analytic_account_python_code = fields.Text(
        string="Analytic Account Python Code",
        default="result = []",
        help="Python code used to compute the analytic accounts allowed on "
        "payslips of this type when 'Analytic Account Selection Method' is "
        "set to 'Python Code'.",
    )
    debit_usage_selection_method = fields.Selection(
        string="Debit Usage Selection Method",
        selection=M2O_CONFIGURATOR_SELECTION_METHOD,
        default="domain",
        required=True,
        help="Strategy used to compute the debit usages allowed on payslips of "
        "this type. 'Manual' uses 'Debit Usages', 'Domain' evaluates 'Debit "
        "Usage Domain', 'Python Code' evaluates 'Debit Usage Python Code'.",
    )
    debit_usage_ids = fields.Many2many(
        string="Debit Usages",
        comodel_name="product.usage_type",
        relation="rel_payslip_type_2_debit_usage",
        column1="type_id",
        column2="usage_id",
        help="Product usage types allowed as debit usage on payslips of this "
        "type when 'Debit Usage Selection Method' is set to 'Manual'.",
    )
    debit_usage_domain = fields.Text(
        string="Debit Usage Domain",
        default="[]",
        help="Domain used to filter the debit usages allowed on payslips of "
        "this type when 'Debit Usage Selection Method' is set to 'Domain'.",
    )
    debit_usage_python_code = fields.Text(
        string="Debit Usage Python Code",
        default="result = []",
        help="Python code used to compute the debit usages allowed on payslips "
        "of this type when 'Debit Usage Selection Method' is set to "
        "'Python Code'.",
    )
    credit_usage_selection_method = fields.Selection(
        string="Credit Usage Selection Method",
        selection=M2O_CONFIGURATOR_SELECTION_METHOD,
        default="domain",
        required=True,
        help="Strategy used to compute the credit usages allowed on payslips "
        "of this type. 'Manual' uses 'Credit Usages', 'Domain' evaluates "
        "'Credit Usage Domain', 'Python Code' evaluates 'Credit Usage Python "
        "Code'.",
    )
    credit_usage_ids = fields.Many2many(
        string="Credit Usages",
        comodel_name="product.usage_type",
        relation="rel_payslip_type_2_credit_usage",
        column1="type_id",
        column2="usage_id",
        help="Product usage types allowed as credit usage on payslips of this "
        "type when 'Credit Usage Selection Method' is set to 'Manual'.",
    )
    credit_usage_domain = fields.Text(
        string="Credit Usage Domain",
        default="[]",
        help="Domain used to filter the credit usages allowed on payslips of "
        "this type when 'Credit Usage Selection Method' is set to 'Domain'.",
    )
    credit_usage_python_code = fields.Text(
        string="Credit Usage Python Code",
        default="result = []",
        help="Python code used to compute the credit usages allowed on "
        "payslips of this type when 'Credit Usage Selection Method' is set "
        "to 'Python Code'.",
    )
    employee_selection_method = fields.Selection(
        string="Employee Selection Method",
        selection=M2O_CONFIGURATOR_SELECTION_METHOD,
        default="domain",
        required=True,
        help="Strategy used to compute the employees allowed on payslips of "
        "this type. 'Manual' uses 'Employees', 'Domain' evaluates 'Employee "
        "Domain', 'Python Code' evaluates 'Employee Python Code'.",
    )
    employee_ids = fields.Many2many(
        string="Employees",
        comodel_name="hr.employee",
        relation="rel_payslip_type_2_employee",
        column1="type_id",
        column2="employee_id",
        help="Employees allowed to be assigned a payslip of this type when "
        "'Employee Selection Method' is set to 'Manual'.",
    )
    employee_domain = fields.Text(
        string="Employee Domain",
        default="[]",
        help="Domain used to filter the employees allowed to be assigned a "
        "payslip of this type when 'Employee Selection Method' is set to "
        "'Domain'.",
    )
    employee_python_code = fields.Text(
        string="Employee Python Code",
        default="result = []",
        help="Python code used to compute the employees allowed to be "
        "assigned a payslip of this type when 'Employee Selection Method' "
        "is set to 'Python Code'.",
    )
