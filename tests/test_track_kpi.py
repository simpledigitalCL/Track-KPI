# -*- coding: utf-8 -*-
# Track KPI · Simplefy™
# © Simpledigital SpA — www.simpledigital.cl
# SPDX-License-Identifier: LGPL-3.0
# =============================================================================
# Tests multi-moneda para Track KPI.
# Multi-currency tests for Track KPI discount KPIs.
# =============================================================================

from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestTrackKpi(common.TransactionCase):
    """Tests multi-moneda para KPIs de descuento.
       Multi-currency tests for discount KPIs."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.InvoiceReport = cls.env['account.invoice.report']
        cls.Partner = cls.env['res.partner']
        cls.Product = cls.env['product.product']
        cls.AccountMove = cls.env['account.move']

        # Monedas / Currencies
        cls.clp = cls.env.ref('base.CLP')
        cls.usd = cls.env.ref('base.USD')
        cls.eur = cls.env.ref('base.EUR')

        # Partner y producto genérico / Generic partner & product
        cls.partner = cls.Partner.create({'name': 'Test TrackKPI'})
        cls.product = cls.Product.create({
            'name': 'Producto Test KPI',
            'type': 'consu',
            'list_price': 1000,
        })

    # ── Helpers ─────────────────────────────────────────
    def _create_invoice(self, currency, price_unit, discount=0.0):
        """Crea y postea factura de prueba.
           Creates and posts a test invoice."""
        move = self.AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': currency.id,
            'invoice_date': '2026-06-01',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'name': 'Línea test / Test line',
                'quantity': 1,
                'price_unit': price_unit,
                'discount': discount,
            })],
        })
        move.action_post()
        self.env.flush_all()
        return move

    def _get_report_line(self):
        """Devuelve la línea del informe para el partner de test.
           Returns the report line for the test partner."""
        return self.InvoiceReport.search(
            [('partner_id', '=', self.partner.id)], limit=1
        )

    # ── CLP: casos base / base cases ───────────────────
    def test_clp_no_discount(self):
        """Sin descuento: subtotal = precio, impacto = 0.
           No discount: subtotal = price, impact = 0."""
        self._create_invoice(self.clp, 1000, discount=0)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertAlmostEqual(r.kpi_subtotal_list_price, 1000, places=0)
        self.assertAlmostEqual(r.kpi_discount_impact, 0, places=0)
        self.assertEqual(r.kpi_discount_percent, 0)

    def test_clp_10_percent_discount(self):
        """10 % descuento: neto 900, subtotal 1000, impacto 100.
           10 % discount: net 900, subtotal 1000, impact 100."""
        self._create_invoice(self.clp, 1000, discount=10)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertAlmostEqual(r.kpi_discount_percent, 10, places=0)
        self.assertAlmostEqual(r.kpi_subtotal_list_price, 1000, places=0)
        self.assertAlmostEqual(r.kpi_discount_impact, 100, places=0)

    def test_clp_100_percent_discount(self):
        """100 % descuento: subtotal 0, impacto 0.
           100 % discount: subtotal 0, impact 0."""
        self._create_invoice(self.clp, 1000, discount=100)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertEqual(r.kpi_discount_percent, 100)
        self.assertEqual(r.kpi_subtotal_list_price, 0.0)
        self.assertEqual(r.kpi_discount_impact, 0.0)

    # ── Multi-moneda / Multi-currency ───────────────────
    def test_usd_price_unit_converted(self):
        """Precio USD convertido a moneda reporte.
           USD price converted to report currency."""
        self._create_invoice(self.usd, 10, discount=0)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertGreater(r.kpi_price_unit, 100,
            '10 USD debe ser > 100 CLP al convertir / 10 USD should be > 100 CLP after conversion')
        self.assertEqual(r.kpi_currency_id, self.usd)

    def test_currency_field_matches_invoice_currency(self):
        """kpi_currency_id coincide con moneda de la factura.
           kpi_currency_id matches the invoice currency."""
        self._create_invoice(self.eur, 100, discount=5)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertEqual(r.kpi_currency_id.id, self.eur.id)

    def test_multi_currency_discount_formulas_consistent(self):
        """Fórmulas consistentes con descuento en USD.
           Consistent formulas with USD discount."""
        self._create_invoice(self.usd, 50, discount=20)
        r = self._get_report_line()
        self.assertTrue(r)
        self.assertAlmostEqual(r.kpi_discount_percent, 20, places=0)
        self.assertGreater(r.kpi_subtotal_list_price, 0,
            'Subtotal sin descuento debe ser > 0 / Subtotal before discount must be > 0')
        self.assertGreater(r.kpi_discount_impact, 0,
            'Impacto descuento debe ser > 0 / Discount impact must be > 0')
