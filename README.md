# Track KPI — Simplefy™

**KPIs de descuento sobre facturación estándar de Odoo.**
*Discount KPIs on Odoo's standard invoice report.*

Multi-moneda · Odoo 18 / 19 · [simpledigital.cl](https://simpledigital.cl)

---

## Qué hace / What it does

Extiende `account.invoice.report` con 5 campos quirúrgicos.
*Extends `account.invoice.report` with 5 surgical fields.*

| Campo / Field | Descripción / Description |
|---|---|
| Descuento línea (%) | Porcentaje de descuento por línea / Line discount percentage |
| Precio unitario | Precio de lista a moneda de reporte / List price in report currency |
| Subtotal sin descuento | Valor antes del descuento / Value before discount |
| Impacto descuento | Monto total del descuento / Total discount amount |
| Moneda factura | Moneda original (trazabilidad) / Original currency (traceability) |

Compatible multi-moneda: CLP, USD, EUR, etc. Los valores se convierten
automáticamente a la moneda de reporte.
*Multi-currency: values are automatically converted to report currency.*

---

## Instalación / Installation

1. Copiar `track_kpi/` en `addons/` / *Copy `track_kpi/` into `addons/`*
2. Actualizar lista de módulos / *Update apps list*
3. Instalar «Track KPI» / *Install "Track KPI"*

Odoo.sh: agregar repo como submódulo.
*Odoo.sh: add repo as submodule.*

---

## Uso / Usage

**TrackKPI → Facturación y descuentos**

Vistas: lista, pivot, gráfico. En pivot: % descuento = **promedio**,
importes = **suma**.
*Views: list, pivot, graph. In pivot: % discount =* **average**,
*amounts =* **sum**.

---

## Licencia / License

LGPL-3.0 © Simpledigital SpA — [simpledigital.cl](https://simpledigital.cl)

---

## Soporte / Support

Comercial, implementación, personalización:
*Commercial, implementation, customization:*
[soporte@simpledigital.cl](mailto:soporte@simpledigital.cl)
