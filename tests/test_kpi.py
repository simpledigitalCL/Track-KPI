# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged
from odoo import Command


@tagged('post_install', '-at_install')
class TestTrackKPI(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['res.currency.rate'].create({
            'name': '2026-01-01',
            'currency_id': cls.env.ref('base.USD').id,
            'rate': 0.0011,
        })
        cls.partner = cls.env['res.partner'].create({'name': 'KPI Test Partner'})
        cls.product = cls.env['product.product'].create({
            'name': 'KPI Test Product', 'type': 'consu', 'list_price': 10000})

    def _create_invoice(self, price_unit, quantity, discount):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice', 'partner_id': self.partner.id,
            'invoice_date': '2026-06-01',
            'invoice_line_ids': [Command.create({
                'product_id': self.product.id,
                'price_unit': price_unit, 'quantity': quantity,
                'discount': discount})]})
        move.action_post()
        self.env['account.invoice.report'].flush_model()
        return move

    def _kpi(self, move):
        self.env['account.invoice.report'].flush_model()
        r = self.env['account.invoice.report'].search(
            [('move_id', '=', move.id)], limit=1)
        self.assertTrue(r, 'El reporte debe tener al menos una linea')
        return r

    def test_01_no_discount(self):
        r = self._kpi(self._create_invoice(10000, 1, 0))
        self.assertEqual(r.kpi_discount_percent, 0.0)
        self.assertAlmostEqual(r.kpi_subtotal_list_price, 10000, places=2)
        self.assertAlmostEqual(r.kpi_discount_impact, 0.0, places=2)

    def test_02_50_percent(self):
        r = self._kpi(self._create_invoice(20000, 1, 50))
        self.assertEqual(r.kpi_discount_percent, 50.0)
        self.assertAlmostEqual(r.kpi_subtotal_list_price, 20000, places=2)
        self.assertAlmostEqual(r.kpi_discount_impact, 10000, places=2)

    def test_03_100_percent(self):
        r = self._kpi(self._create_invoice(5000, 1, 100))
        self.assertEqual(r.kpi_discount_percent, 100.0)
        self.assertAlmostEqual(r.kpi_subtotal_list_price, 0.0, places=2)
        self.assertAlmostEqual(r.kpi_discount_impact, 0.0, places=2)

    def test_04_multiline(self):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice', 'partner_id': self.partner.id,
            'invoice_date': '2026-06-01',
            'invoice_line_ids': [
                Command.create({'product_id': self.product.id,
                    'price_unit': 1000, 'quantity': 10, 'discount': 0}),
                Command.create({'product_id': self.product.id,
                    'price_unit': 1000, 'quantity': 1, 'discount': 50})]})
        move.action_post()
        self.env['account.invoice.report'].flush_model()
        lines = self.env['account.invoice.report'].search(
            [('move_id', '=', move.id)])
        self.assertEqual(len(lines), 2)
        l1 = lines.filtered(lambda l: l.kpi_discount_percent == 0.0)
        l2 = lines.filtered(lambda l: l.kpi_discount_percent == 50.0)
        self.assertTrue(l1 and l2)
        self.assertAlmostEqual(l1.kpi_subtotal_list_price, 10000, places=2)
        self.assertAlmostEqual(l2.kpi_subtotal_list_price, 1000, places=2)
        self.assertAlmostEqual(l2.kpi_discount_impact, 500, places=2)

    def test_05_price_unit_preserved(self):
        r = self._kpi(self._create_invoice(12345.6789, 2, 10))
        self.assertAlmostEqual(r.kpi_price_unit, 12345.6789, places=4)
