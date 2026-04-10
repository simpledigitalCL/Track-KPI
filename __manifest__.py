{
    'name': 'Track KPI',
    'version': '1.3.2',
    'summary': 'KPIs sobre el informe estándar de facturas (account.invoice.report) y descuentos por línea',
    'author': 'Simpledigital',
    'category': 'Accounting',
    'depends': ['account', 'sale'],
    'data': [
        'views/invoice_report_views.xml',
    ],
    # Icono: colocar PNG cuadrado (256×256 o 512×512) en static/description/icon.png y commitearlo (Odoo.sh).
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
