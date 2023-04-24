# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Multiple Branch Unit Operation Setup for Helpdesk',
    'version': '16.0.0.0',
    'category': 'Extra Tools',
    'author': 'BrowseInfo',
    'summary': 'Multiple Branch Management helpdesk Multi Branch app service desk Multiple Unit Operating unit desk branch service branch CRM helpdesk system branch CRM branch helpdesk branch service for single company with Multi Branches multi company',
    "description": """
       Multiple Unit operation management for single company, Mutiple Branch management for single company, multiple operation for single company.
    Branch for POS, Branch for Sales, Branch for Purchase, Branch for all, Branch for Accounting, Branch for invoicing, Branch for Payment order, Branch for point of sales, Branch for voucher, Branch for All Accounting reports, Branch Accounting filter.Branch for warehouse, branch for sale stock, branch for location
  Unit for POS, Unit for Sales, Unit for Purchase, Unit for all, Unit for Accounting, Unit for invoicing, Unit for Payment order, Unit for point of sales, Unit for voucher, Unit for All Accounting reports, Unit Accounting filter.branch unit for warehouse, branch unit for sale stock, branch unit for location
  Unit Operation for POS, Unit Operation for Sales, Unit operation for Purchase, Unit operation for all, Unit operation for Accounting, Unit Operation for invoicing, Unit operation for Payment order, Unit operation for point of sales, Unit operation for voucher, Unit operation for All Accounting reports, Unit operation Accounting filter.
  Branch Operation for POS, Branch Operation for Sales, Branch operation for Purchase, Branch operation for all, Branch operation for Accounting, Branch Operation for invoicing, Branch operation for Payment order, Branch operation for point of sales, Branch operation for voucher, Branch operation for All Accounting reports, Branch operation Accounting filter.


       operating unit for company.
       Multiple Branch Operation Setup for customer
       Unit Operation Setup for helpdesk

       Multiple Branch Operation Setup for helpdesk
       Unit Operation Setup for helpdesk
       multiple branch for CRM helpdesk
       multiple branch for helpdesk
       multiple branch for customer helpdesk
       multiple branch for helpdesk customer support
       multiple branch for Customer relationship management
       multiple branch for Customer helpdesk management
       multiple branch for support
       multiple branch for sales team
       multiple branch for Sale and CRM
       multiple branch for CRM Contacts
       multiple branch for CRM customer
       multiple branch for Contacts
       multiple branch for customer

       multiple Unit Operation for helpdesk
       multiple Unit Operation for CRM helpdesk
       multiple Unit Operation for customer helpdesk
       multiple Unit Operation for CRM Sales
       multiple Unit Operation for Customer relationship management
       multiple Unit Operation for Lead
       multiple Unit Operation for Oppertunity
       multiple Unit Operation for sales team
       multiple Unit Operation for Sale and CRM
       multiple Unit Operation for CRM Contacts
       multiple Unit Operation for CRM customer
       multiple Unit Operation for Contacts
       multiple Unit Operation for customer
       branch helpdesk and support
       branch support and helpdesk
       helpdesk branch
       helpdesk unit 
       helpdek multiple unit
       helpdesk operation unit
       multi branch management
       multi branch application
       multi operation unit application multi branch odoo multi branch
       all in one multi branch application multi branch unit operation multi unit operation branch management
       odoo multi branches management application multi operation mangement
    """,
    'website': 'https://www.browseinfo.in',
    'depends': ['base','helpdesk','helpdesk_sale_timesheet','branch'],
    'uninstall_hook': '_uninstall_hook',
    'data': [   
                'security/helpdesk_security.xml',
                'views/helpdesk_branch_view.xml',
                'report/helpdesk_report_view.xml',
             ],
    'qweb': [],
    'demo': [],
    "price": 19.00,
    "currency": 'EUR',
    'test': [],
    'license':'OPL-1',
    'installable': True,
    'live_test_url':'https://youtu.be/Dr7xMlLmRWg',
    'auto_install': False,
    "images":['static/description/Banner.gif'],
}


