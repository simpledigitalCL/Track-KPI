# -*- coding: utf-8 -*-
# Track KPI · Simplefy™
# © Simpledigital SpA — www.simpledigital.cl
# SPDX-License-Identifier: LGPL-3.0
# =============================================================================
# Extiende account.invoice.report con 4 KPIs de descuento + trazabilidad de
# moneda. Compatible multi-moneda (CLP, USD, EUR, etc.).
#
# Extends account.invoice.report with 4 discount KPIs + currency traceability.
# Multi-currency ready (CLP, USD, EUR, etc.).
# =============================================================================

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    # ── Campos KPI / KPI Fields ─────────────────────────
    kpi_discount_percent = fields.Float(
        string='Descuento línea (%) / Line discount (%)',
        readonly=True,
        aggregator='avg',
        digits=(16, 2),
        help='Porcentaje de descuento por línea. En pivot: promedio (avg). / '
             'Line discount percentage. In pivot: average (avg).',
    )
    kpi_price_unit = fields.Float(
        string='Precio unitario / Unit price',
        readonly=True,
        digits=(16, 4),
        help='Precio de lista convertido a moneda de reporte (multi-moneda). / '
             'List price converted to report currency (multi-currency).',
    )
    kpi_subtotal_list_price = fields.Float(
        string='Subtotal sin descuento / Subtotal before discount',
        readonly=True,
        aggregator='sum',
        digits=(16, 2),
        help='Valor antes del descuento, en moneda de reporte. / '
             'Value before discount, in report currency.',
    )
    kpi_discount_impact = fields.Float(
        string='Impacto descuento / Discount impact',
        readonly=True,
        aggregator='sum',
        digits=(16, 2),
        help='Monto total del descuento aplicado, en moneda de reporte. / '
             'Total discount amount applied, in report currency.',
    )
    kpi_currency_id = fields.Many2one(
        'res.currency',
        string='Moneda factura / Invoice currency',
        readonly=True,
        help='Moneda original de la factura. Trazabilidad multi-moneda. / '
             'Original invoice currency. Multi-currency traceability.',
    )

    # ── SQL ──────────────────────────────────────────────
    # account.invoice.report es _auto=False → todo se define en _select().
    # account_currency_table convierte montos a la moneda de reporte.
    # line.balance = neto por línea (incluye impuestos si price-included).
    #
    # account.invoice.report uses _auto=False → everything via _select().
    # account_currency_table converts amounts to report currency.
    # line.balance = net line amount (includes taxes if price-included).
    # ──────────────────────────────────────────────────────
    @api.model
    def _select(self) -> SQL:
        return SQL(
            """
            %s,
            line.discount AS kpi_discount_percent,
            line.price_unit * account_currency_table.rate AS kpi_price_unit,
            move.currency_id AS kpi_currency_id,
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

    # ── Acción / Action ──────────────────────────────────
    def action_open_move(self):
        """Abre la factura original desde el informe.
           Opens the source invoice from the report line."""
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
