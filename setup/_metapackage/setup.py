import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-hr-payroll",
    description="Meta package for open-synergy-opnsynid-hr-payroll Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_hr_payroll',
        'odoo14-addon-ssi_hr_payroll_batch',
        'odoo14-addon-ssi_hr_payroll_batch_work_log',
        'odoo14-addon-ssi_hr_payroll_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
