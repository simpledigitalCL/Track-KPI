{
    'name': 'Track KPI',
    'version': '1.3.4',
    'summary': 'KPIs sobre el informe estándar de facturas (account.invoice.report) y descuentos por línea',
    'author': 'Simpledigital',
    'category': 'Accounting',
    'depends': ['account', 'sale'],
    'data': [
        'views/invoice_report_views.xml',
    ],
    # Icono del módulo (Apps): debe existir en el repo; WebP suele ir bien en Odoo 18+.
    'images': ['static/description/icon.webp'],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
