{
    'name': 'Track KPI',
    'version': '1.3.7',
    'summary': 'KPIs sobre el informe estándar de facturas (account.invoice.report) y descuentos por línea',
    'author': 'Simpledigital',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'depends': ['account', 'sale'],
    'data': [
        'views/invoice_report_views.xml',
    ],
    # Odoo.sh valida icono en PNG (cuadrado); WebP opcional como segundo recurso.
    'images': [
        'static/description/icon.png',
        'static/description/icon.webp',
    ],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
