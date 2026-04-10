from . import models


def post_init_hook(env):
    """Odoo 18+: el hook recibe env (antes cr, registry)."""
    env.cr.execute('DROP VIEW IF EXISTS track_kpi_invoice_report')
