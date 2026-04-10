def migrate(cr, installed_version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    data = env['ir.model.data'].sudo().search([
        ('model', '=', 'ir.ui.menu'),
        ('name', '=', 'menu_track_kpi_root'),
    ], limit=1)
    if not data:
        return
    menu = env['ir.ui.menu'].browse(data.res_id).exists()
    if not menu:
        return
    mod = data.module
    menu.write({'web_icon': False})
    menu.write({'web_icon': '%s,static/description/icon.png' % mod})
