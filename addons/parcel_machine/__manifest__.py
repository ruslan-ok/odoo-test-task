# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Delivery InPost',
    'version': '1.0',
    'author': 'Ruslan Akunevich',
    'category': 'Customizations',
    'summary': 'Parcel Machine list, Sale Orders, Delivery control',
    'description': 'This module allows deliver the purchase to a parcel machine.',
    'depends': ['base', 'sale'],
    'data': [
        'security/parcel_machine_groups.xml',
        'security/ir.model.access.csv',
        'data/parcel.machine.csv',
        'data/parcel_machine_cron.xml',
        'views/parcel_machine_views.xml',
        'views/sale_order_views.xml',
        'views/sale_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
