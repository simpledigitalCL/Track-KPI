{
    'name': 'Track KPI',
    'version': '1.1.1',
    'summary': 'KPIs comerciales y análisis de descuentos en facturas',
    'author': 'Simpledigital',
    'category': 'Sales',
    'depends': ['account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_report_views.xml',
    ],
    'application': True,
    'installable': True,
}
