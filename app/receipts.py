from escpos.escpos import Escpos
from pydantic import BaseModel

import logging

from app.utils import format_table_line

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

NORMAL = {"bold": False, "align": "center", "custom_size": True, "height": 2, "width": 1}
NORMAL_LEFT = {"bold": False, "align": "left", "custom_size": True, "height": 2, "width": 1}
NORMAL_BOLD = {"bold": True, "align": "center", "custom_size": True, "height": 2, "width": 1}
SMALL = {"bold": False, "align": "center", "custom_size": True, "height": 1, "width": 1}
SMALL_BOLD = {"bold": True, "align": "center", "custom_size": True, "height": 1, "width": 1}

def print_receipt(p: Escpos, receipt: Receipt):
    try:
        p.ln(3)

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
        p.textln(f"CLIENTE: {receipt.cliente}")
        p.textln(f"NIT/CI/CEX: {receipt.nit_cliente}")
        p.textln(f"FECHA DE EMISIÓN: {receipt.fecha_emision}")
        p.textln('-' * 38)

        p.set(**NORMAL_BOLD)
        p.textln("DETALLE")

        p.set(**SMALL_BOLD)
        p.textln(format_table_line("CANT", "DESCRIPCION", "P/U", "SUBTOTAL", is_header=True))

        p.set(**SMALL)

        for item in receipt.items:
            p.textln(format_table_line(
                str(item.cantidad), item.descripcion, str(item.precio_unitario), str(item.subtotal)
            ))

        p.textln('-' * 38)



        p.ln

        p.cut()

        return True

    except Exception as e:
        logging.exception(f"Error printing order: {e}")
        return False
