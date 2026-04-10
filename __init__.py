from . import models


def post_init_hook(*args, **kwargs):
    """Compatible con Odoo 18+ (solo env) y versiones que pasan (cr, registry)."""
    if not args:
        return
    arg0 = args[0]
    cr = arg0.cr if hasattr(arg0, 'cr') else arg0
    cr.execute('DROP VIEW IF EXISTS track_kpi_invoice_report')
