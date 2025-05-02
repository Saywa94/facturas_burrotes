from flask import Blueprint

from app.orders import Order, OrderItem
from app.receipts import Receipt, ReceiptItem

from .printers import check_both, print, test_print

bp = Blueprint("main", __name__)

@bp.route('/')
def hello_world():
    return 'Hello, Fusi!'

@bp.route('/test', methods=['POST', 'GET'])
def test():

    test_print("cashier")

    return {"status": "ok"}

@bp.route('/check_printers', methods=['GET'])
def check_printers():
    success, offline_printer = check_both()

    status = "ok" if success else "not_connected"
    return {"status": status, "offline_printer": offline_printer}


@bp.route('/print_receipt', methods=['POST', 'GET'])
def print_receipt_route():

    receipt = Receipt(
        number = 28,
        razon_social = "Grupo GFV S.R.L.",
        numero_sucursal = 1,
        punto_venta = 1,
        direccion_sucursal = "3, Avenida Costanera, zona Irpavi",
        municipio = "La Paz",
        nit = 620466028,
        number_factura = 1,
        codigo_autorizacion = "123456789",
        fecha_emision = "01/05/2025",
        cliente = "Giuseppe Fusi",
        nit_cliente = 68770242,
        items = [
            ReceiptItem(
                cantidad=2,
                descripcion="Burro M Pollo",
                precio_unitario=25,
                subtotal=50
            ),
            ReceiptItem(
                cantidad=1,
                descripcion="Bowl XL Pollo Carne Chorizo",
                precio_unitario=45,
                subtotal=45
            ),
            ReceiptItem(
                cantidad=3,
                descripcion="CocaCola 500ml",
                precio_unitario=10,
                subtotal=30
            ),
        ],
        subtotal = 125,
        descuento = 0,
        total = 125,
        total_iva = 125,
        total_escrito = "ciento veinticinco bolivianos",
        qr_code = "https://siat.impuestos.gob.bo/consulta/QR?nit=3423421013&cuf=EA3D6EBF506FCFD1FC42E2F1997F1333117CD97DE562A03052E349E74&numero=19&t=1",
        leyenda_1 = "ESTA FACTURA CONTRIBUYE AL DESARROLLO DEL PAÍS, EL USO ILÍCITO SERÁ SANCIONADO PENALMENTE DE ACUERDO A LEY",
        leyenda_2 = "Ley N° 453: El proveedor deberá entregar el producto en las modalidades y términos ofertados o convenidos.",
        leyenda_3 = '"Este documento es la Representación Gráfica de un Documento Fiscal Digital emitido en una modalidad de facturación en línea"'
    )

    if not print("cashier", receipt):
        return {
            "status": "error",
            "message": "No se pudo imprimir la factura"
        }

    res = {
        "status": "ok",
        "message": "Factura impresa exitosamente"
    }
    return res

@bp.route('/print_order', methods=['POST', 'GET'])
def print_order_route():
    order = Order(
        number = 28,
        customer = None,
        date_time = "24/04/2025 - 19:30:25",
        dine_in = [
            OrderItem(
                quantity=1,
                product="Burro M - Pollo",
                details = "Queso, Mayo, Spicy", 
                extra = None,
                is_cooked=True
            ),
            OrderItem(quantity=1, product="Bowl L - Carne, Chori", details = "Queso, Curry, Ketchup, Burguer", extra = None, is_cooked=True),
            OrderItem(
                quantity=2,
                product="CocaCola 500ml",
                details = None, 
                extra = None,
                is_cooked=False
            ),
        ],
        take_out = [
            OrderItem(
                quantity=1,
                product="Burro M - Pollo",
                details = "Queso, Mayo, Spicy", 
                extra = None,
                is_cooked=True
            ),
            OrderItem(quantity=1, product="Bowl L - Carne, Chori", details = "Queso, Curry, Ketchup, Burguer", extra = None, is_cooked=True),
            OrderItem(
                quantity=2,
                product="CocaCola 500ml",
                details = None, 
                extra = None,
                is_cooked=False
            ),
        ],
        beeper = 8,
        comment = "Poquito picante porfavor"
    )

    if not print("kitchen", order):
        return {
            "status": "error",
            "message": "No se pudo imprimir el pedido"
        }

    res = {
        "status": "ok",
        "message": "Pedido impreso exitosamente"
    }
    return res
