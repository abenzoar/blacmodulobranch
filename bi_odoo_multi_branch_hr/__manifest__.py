# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Multiple Branch(Unit) Operation Setup for Human Resource Odoo/OpenERP',
    'version': '16.0.0.1',
    'category': 'Human Resource',
    'summary': 'Multiple Branch Management HR Multi Branch HR Employee app Multiple Unit operation for human resource multi branch HR operation multi branch hr Department branch Payslip Reports for single company Multi Branch employee multi branch for hr multiple branch',
    "description": """
       Multiple Unit operation management for single company, Mutiple Branch management for single company, multiple operation for single company.
    Branch for POS, Branch for Sales, Branch for Purchase, Branch for all, Branch for Accounting, Branch for invoicing, Branch for Payment order, Branch for point of sales, Branch for voucher, Branch for All Accounting reports, Branch Accounting filter.Branch for warehouse, branch for sale stock, branch for location
  Unit for POS, Unit for Sales, Unit for Purchase, Unit for all, Unit for Accounting, Unit for invoicing, Unit for Payment order, Unit for point of sales, Unit for voucher, Unit for All Accounting reports, Unit Accounting filter.branch unit for warehouse, branch unit for sale stock, branch unit for location
  Unit Operation for POS, Unit Operation for Sales, Unit operation for Purchase, Unit operation for all, Unit operation for Accounting, Unit Operation for invoicing, Unit operation for Payment order, Unit operation for point of sales, Unit operation for voucher, Unit operation for All Accounting reports, Unit operation Accounting filter.
  Branch Operation for POS, Branch Operation for Sales, Branch operation for Purchase, Branch operation for all, Branch operation for Accounting, Branch Operation for invoicing, Branch operation for Payment order, Branch operation for point of sales, Branch operation for voucher, Branch operation for All Accounting reports, Branch operation Accounting filter.


       operating unit for company.
       Multiple Branch Operation Setup for Human Resource
       Unit Operation Setup for Human Resource

       Multiple Branch Operation Setup for HR
       Unit Operation Setup for HR
       multiple branch for HR Employee
       multiple branch for HR Application
       multiple branch for HR Contract
       multiple branch for HR Expense
       multiple branch for HR Payslip
       multiple branch for HR Leaves
       multiple branch for HR Holiday
       multiple branch for HR Department
       multiple branch for HR Attandance

       Unit Operation for HR Employee
       multiple Unit Operation for HR Application
       multiple Unit Operation for HR Contract
       multiple Unit Operation for HR Expense
       multiple Unit Operation for HR Payslip
       multiple Unit Operation for HR Leaves
       multiple Unit Operation for HR Holiday
       multiple Unit Operation for HR Department
       multiple Unit Operation for HR Attandance

       multiple branch for Employee
       multiple branch for Application
       multiple branch for Contract
       multiple branch for Expense
       multiple branch for Payslip
       multiple branch for Leaves
       multiple branch for Holiday
       multiple branch for Department
       multiple branch for Attandance

       multiple Unit Operation for Employee
       multiple Unit Operation for Application
       multiple Unit Operation for Contract
       multiple Unit Operation for Expense
       multiple Unit Operation for Payslip
       multiple Unit Operation for Leaves
       multiple Unit Operation for Holiday
       multiple Unit Operation for Department
       multiple Unit Operation for Attandance
       branch hr
       hr branch
       hr operating unit
       hr unit operation management
      hr multiple unit
       operating unit hr
       branch Human Resource
       Human Resource branch
       Human Resource operating unit
       Human Resource unit operation management
      Human Resource multiple unit
       operating unit Human Resource
       multi branch management
       multi branch application
       multi operation unit application multi branch odoo multi branch
       all in one multi branch application multi branch unit operation multi unit operation branch management
       odoo multi branches management application multi operation mangement


operating Unit for POS,operating Unit for Sales,operating Unit for Purchase,operating Unit for all,operating Unit for Accounting,operating Unit for invoicing,operating Unit for Payment order,operating Unit for point of sales,operating Unit for voucher,operating Unit for All Accounting reports,operating Unit Accounting filter. Operating unit for picking, operating unit for warehouse, operaing unit for sale stock, operating unit for location
operating-Unit Operation for POS,operating-Unit Operation for Sales,operating-Unit operation for Purchase,operating-Unit operation for all, operating-Unit operation for Accounting,operating-Unit Operation for invoicing,operating-Unit operation for Payment order,operating-Unit operation for point of sales,operating-Unit operation for voucher,operating-Unit operation for All Accounting reports,operating-Unit operation Accounting filter.
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    "price": 40.00,
    'license': 'OPL-1',
    "currency": 'EUR',
    'depends': ['base','branch','hr_attendance','hr_recruitment','hr_contract','hr_expense','hr_payroll'],
    'data': [
                'security/hr_branch_security.xml',
                'views/hr_branch_view.xml',
                'report/hr_payslip_details_view.xml',
             ],
    'qweb': [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/K6RmQEKtWeY',
    "images":['static/description/Banner.gif'],
}


