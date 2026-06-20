# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    kpi_discount_percent = fields.Float(
        string='Descuento linea (%)', readonly=True, aggregator='avg', digits=(16, 2),
        help='Porcentaje de descuento por linea de factura. En vistas pivot el agregado es PROMEDIO SIMPLE (avg), no ponderado por monto. Para el impacto real en $, usar Impacto descuento. Un promedio alto con impacto bajo sugiere descuentos concentrados en lineas de bajo valor.')
    kpi_price_unit = fields.Float(string='Precio unitario (lista)', readonly=True, digits=(16, 4))
    kpi_subtotal_list_price = fields.Float(string='Subtotal sin descuento (sin impuestos)', readonly=True, aggregator='sum', digits=(16, 2))
    kpi_discount_impact = fields.Float(string='Impacto descuento (sin impuestos)', readonly=True, aggregator='sum', digits=(16, 2))

    @api.model
    def _select(self) -> SQL:
        return SQL(
            """
            %s,
            line.discount AS kpi_discount_percent,
            line.price_unit AS kpi_price_unit,
            CASE
                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0
                ELSE (-line.balance * COALESCE(account_currency_table.rate, 1.0))
                     / NULLIF(1.0 - line.discount / 100.0, 0.0)
            END AS kpi_subtotal_list_price,
            CASE
                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0
                ELSE (-line.balance * COALESCE(account_currency_table.rate, 1.0))
                     * (line.discount / 100.0)
                     / NULLIF(1.0 - line.discount / 100.0, 0.0)
            END AS kpi_discount_impact
            """,
            super()._select())

    def action_open_move(self):
        self.ensure_one()
        move = self.move_id
        if not move:
            return False
        return {'type': 'ir.actions.act_window', 'name': move.display_name,
                'res_model': 'account.move', 'res_id': move.id,
                'view_mode': 'form', 'views': [(False, 'form')], 'target': 'current'}
