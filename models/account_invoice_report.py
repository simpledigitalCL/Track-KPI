# -*- coding: utf-8 -*-
# Odoo 18 / 19: account.invoice.report usa odoo.tools.SQL y account_currency_table.
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    kpi_discount_percent = fields.Float(
        string='Descuento línea (%)',
        readonly=True,
        aggregator='avg',
        digits=(16, 2),
        help='En vista pivot, el agregado por defecto de esta medida es el promedio (avg), '
             'coherente con un porcentaje por línea.',
    )
    kpi_price_unit = fields.Float(
        string='Precio unitario (lista)',
        readonly=True,
        digits=(16, 4),
    )
    kpi_subtotal_list_price = fields.Float(
        string='Subtotal sin descuento (sin impuestos)',
        readonly=True,
        aggregator='sum',
        digits=(16, 2),
    )
    kpi_discount_impact = fields.Float(
        string='Impacto descuento (sin impuestos)',
        readonly=True,
        aggregator='sum',
        digits=(16, 2),
    )

    @api.model
    def _select(self) -> SQL:
        return SQL(
            """
            %s,
            line.discount AS kpi_discount_percent,
            line.price_unit AS kpi_price_unit,
            CASE
                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0
                ELSE (-line.balance * account_currency_table.rate)
                     / NULLIF(1.0 - line.discount / 100.0, 0.0)
            END AS kpi_subtotal_list_price,
            CASE
                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0
                ELSE (-line.balance * account_currency_table.rate)
                     * (line.discount / 100.0)
                     / NULLIF(1.0 - line.discount / 100.0, 0.0)
            END AS kpi_discount_impact
            """,
            super()._select(),
        )

    def action_open_move(self):
        """Abre la factura/asiento desde la línea del informe (respaldo si el many2one no navega)."""
        self.ensure_one()
        move = self.move_id
        if not move:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': move.display_name,
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }
