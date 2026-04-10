# -*- coding: utf-8 -*-
# Compatible con Odoo 18 / 19: account.invoice.report usa odoo.tools.SQL y account_currency_table.
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    kpi_discount_percent = fields.Float(
        string='Descuento línea (%)',
        readonly=True,
        aggregator='avg',
    )
    kpi_price_unit = fields.Float(
        string='Precio unitario (lista)',
        readonly=True,
    )
    kpi_subtotal_list_price = fields.Float(
        string='Subtotal sin descuento (sin impuestos)',
        readonly=True,
        aggregator='sum',
    )
    kpi_discount_impact = fields.Float(
        string='Impacto descuento (sin impuestos)',
        readonly=True,
        aggregator='sum',
    )

    @api.model
    def _select(self) -> SQL:
        return SQL(
            '%s,\n'
            '            line.discount AS kpi_discount_percent,\n'
            '            line.price_unit AS kpi_price_unit,\n'
            '            CASE\n'
            '                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0\n'
            '                ELSE (-line.balance * account_currency_table.rate)\n'
            '                     / NULLIF(1.0 - line.discount / 100.0, 0.0)\n'
            '            END AS kpi_subtotal_list_price,\n'
            '            CASE\n'
            '                WHEN COALESCE(line.discount, 0) >= 100 THEN 0.0\n'
            '                ELSE (-line.balance * account_currency_table.rate)\n'
            '                     * (line.discount / 100.0)\n'
            '                     / NULLIF(1.0 - line.discount / 100.0, 0.0)\n'
            '            END AS kpi_discount_impact',
            super()._select(),
        )
