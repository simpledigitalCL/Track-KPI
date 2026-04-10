from odoo import models, fields, tools

class TrackKpiInvoiceReport(models.Model):
    _name = 'track.kpi.invoice.report'
    _description = 'Track KPI Invoice Report'
    _auto = False
    _rec_name = 'invoice_date'

    move_id = fields.Many2one('account.move', string='Factura')
    invoice_date = fields.Date(string='Fecha')
    partner_id = fields.Many2one('res.partner', string='Cliente')
    commercial_partner_id = fields.Many2one('res.partner', string='Cliente Comercial')
    country_id = fields.Many2one('res.country', string='País')

    product_id = fields.Many2one('product.product', string='Producto')
    product_categ_id = fields.Many2one('product.category', string='Categoría')

    invoice_user_id = fields.Many2one('res.users', string='Vendedor')
    team_id = fields.Many2one('crm.team', string='Equipo de ventas')

    company_id = fields.Many2one('res.company', string='Compañía')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    journal_id = fields.Many2one('account.journal', string='Diario')

    move_type = fields.Selection([], string='Tipo')
    state = fields.Selection([], string='Estado')
    payment_state = fields.Selection([], string='Estado de pago')

    quantity = fields.Float(string='Cantidad')
    price_subtotal = fields.Float(string='Subtotal')
    price_total = fields.Float(string='Total')

    price_unit_before_discount = fields.Float(string='Precio Unitario Base')
    discount_percent = fields.Float(string='Descuento (%)')
    discount_amount_unit = fields.Float(string='Descuento Unitario')
    price_unit_after_discount = fields.Float(string='Precio Unitario Final')

    subtotal_before_discount = fields.Float(string='Subtotal sin descuento')
    subtotal_after_discount = fields.Float(string='Subtotal con descuento')

    discount_impact = fields.Float(string='Impacto del descuento')
    discount_ratio = fields.Float(string='Ratio de descuento')

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    line.id as id,
                    move.id as move_id,
                    move.invoice_date,
                    move.partner_id,
                    move.commercial_partner_id,
                    partner.country_id,
                    move.invoice_user_id,
                    move.team_id,
                    move.company_id,
                    move.currency_id,
                    move.journal_id,
                    move.move_type,
                    move.state,
                    move.payment_state,
                    line.product_id,
                    pt.categ_id as product_categ_id,
                    line.quantity,
                    line.price_subtotal,
                    line.price_total,
                    line.price_unit as price_unit_before_discount,
                    line.discount as discount_percent,
                    (line.price_unit * (line.discount / 100.0)) as discount_amount_unit,
                    (line.price_unit * (1 - line.discount / 100.0)) as price_unit_after_discount,
                    (line.price_unit * line.quantity) as subtotal_before_discount,
                    (line.price_unit * (1 - line.discount / 100.0) * line.quantity) as subtotal_after_discount,
                    ((line.price_unit * line.quantity) -
                     (line.price_unit * (1 - line.discount / 100.0) * line.quantity)
                    ) as discount_impact,
                    CASE 
                        WHEN (line.price_unit * line.quantity) = 0 THEN 0
                        ELSE (
                            ((line.price_unit * line.quantity) -
                            (line.price_unit * (1 - line.discount / 100.0) * line.quantity))
                            / (line.price_unit * line.quantity)
                        )
                    END as discount_ratio
                FROM account_move_line line
                JOIN account_move move ON move.id = line.move_id
                LEFT JOIN res_partner partner ON move.partner_id = partner.id
                LEFT JOIN product_product product ON line.product_id = product.id
                LEFT JOIN product_template pt ON product.product_tmpl_id = pt.id
                WHERE move.move_type IN ('out_invoice', 'out_refund')
                AND line.display_type IS NULL
            )
        """)
