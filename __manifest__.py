# -*- coding: utf-8 -*-
# Track KPI · Simplefy™
# © Simpledigital SpA — www.simpledigital.cl
# SPDX-License-Identifier: LGPL-3.0

{
    'name': 'Track KPI',
    'version': '1.4.0',
    'summary': 'KPIs de descuento sobre facturación. Multi-moneda. / '
               'Discount KPIs on invoice report. Multi-currency.',
    'author': 'Simpledigital',
    'website': 'https://simpledigital.cl',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'depends': ['account', 'sale'],
    'data': [
        'views/invoice_report_views.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/icon.webp',
    ],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
