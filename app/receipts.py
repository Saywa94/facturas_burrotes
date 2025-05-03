from escpos.escpos import Escpos
from pydantic import BaseModel

import logging

from pydantic_core import ValidationError

from app.utils import format_table_line, format_totals_line
from app.assets import LOGO_IMAGE

class ReceiptItem(BaseModel):
    cantidad: int
    descripcion: str
    precio_unitario: int
    subtotal: int

class Receipt(BaseModel):
    number: int
    razon_social: str
    numero_sucursal: int
    punto_venta: int
    direccion_sucursal: str
    municipio: str

    nit: int
    number_factura: int
    codigo_autorizacion: str # CUF ??

    fecha_emision: str
    cliente: str
    nit_cliente: int

    items: list[ReceiptItem]

    subtotal: int
    descuento: int
    total: int
    total_iva: int
    total_escrito: str

    qr_code: str
    leyenda_1: str
    leyenda_2: str
    leyenda_3: str

def validate_receipt(data) -> Receipt | None:
    try:
        return Receipt.model_validate(data)
    except ValidationError as e:
        logging.error(e)
        return None


NORMAL = {"font": "a", "bold": False, "align": "center", "custom_size": True, "height": 1, "width": 1}
NORMAL_BOLD = {"font": "a", "bold": True, "align": "center", "custom_size": True, "height": 1, "width": 1}
NORMAL_LEFT = {"font": "a", "bold": False, "align": "left", "custom_size": True, "height": 1, "width": 1}
NORMAL_BOLD_LEFT = {"font": "a", "bold": True, "align": "left", "custom_size": True, "height": 1, "width": 1}
SMALL_CENTER = {"font": "b", "bold": False, "align": "center", "custom_size": True, "height": 1, "width": 1} 

def print_receipt(p: Escpos, receipt: Receipt):
    try:

        p.image(
                img_source=LOGO_IMAGE,
                center=True,
            )
        p.ln()

        p.set(**NORMAL_BOLD)
        p.textln("FACTURA CON DERECHO A CREDITO FISCAL")

        p.set(**NORMAL)
        p.textln(receipt.razon_social)
        p.textln(f"Sucursal No. {receipt.numero_sucursal}")
        p.textln(f"Punto de Venta No. {receipt.punto_venta}")
        p.textln(receipt.direccion_sucursal)
        p.textln(f"{receipt.municipio} - Bolivia")
        p.textln('-' * 38)

        p.set(**NORMAL)
        p.textln(f"NIT: {receipt.nit}")
        p.textln(f"Factura No. {receipt.number_factura}")
        p.textln(f"CÓD. AUTORIZACIÓN: {receipt.codigo_autorizacion}")
        p.textln('-' * 38)

        p.set(**NORMAL_LEFT)
        p.textln(f" CLIENTE: {receipt.cliente}")
        p.textln(f" NIT/CI/CEX: {receipt.nit_cliente}")
        p.textln(f" FECHA DE EMISIÓN: {receipt.fecha_emision}")

        p.set(**NORMAL)
        p.textln('-' * 38)

        p.set(**NORMAL_BOLD)
        p.textln("DETALLE")

        p.set(**NORMAL_BOLD)
        p.textln(format_table_line("CANT", "DESCRIPCION", "P/U", "SUBTOTAL", is_header=True))

        p.set(**NORMAL)

        for item in receipt.items:
            p.textln(format_table_line(
                item.cantidad, item.descripcion, item.precio_unitario, item.subtotal
            ))

        p.textln('-' * 38)
        p.textln(format_totals_line("SUBTOTAL:", receipt.subtotal))
        p.textln(format_totals_line("DESCUENTO:", receipt.descuento))
        p.textln(format_totals_line("TOTAL A PAGAR:", receipt.total))
        p.textln(format_totals_line("IMPORTE BASE A CREDITO FISCAL:", receipt.total))

        p.set(**NORMAL_BOLD_LEFT)
        p.textln(f" SON: {receipt.total_escrito}")

        p.set(**NORMAL)
        p.textln('-' * 38)

        p.qr(
            content=receipt.qr_code,
            size=5,
            center=True,
        )

        p.set(**SMALL_CENTER)
        p.block_text(txt=receipt.leyenda_1, font='b')
        p.ln()
        p.block_text(txt=receipt.leyenda_2, font='b')
        p.ln()
        p.block_text(txt=receipt.leyenda_3, font='b')

        p.ln()

        p.set(**NORMAL)

        p.textln('-' * 38)
        p.textln(f"Pedido: {receipt.number}")
        p.textln('-' * 38)
        p.ln()


        p.cut()

        return True

    except Exception as e:
        logging.exception(f"Error printing order: {e}")
        return False
