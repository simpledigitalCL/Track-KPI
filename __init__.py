from . import models


def post_init_hook(cr, registry):
    cr.execute('DROP VIEW IF EXISTS track_kpi_invoice_report')
