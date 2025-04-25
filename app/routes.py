from flask import Blueprint

from app.orders import Order, OrderItem
from app.receipts import Receipt
from .printers import check_both, print

bp = Blueprint("main", __name__)

@bp.route('/')
def hello_world():
    return 'Hello, Fusi!'

@bp.route('/check_printers', methods=['GET'])
def check_printers():
    success, offline_printer = check_both()

    status = "ok" if success else "not_connected"
    return {"status": status, "offline_printer": offline_printer}


@bp.route('/print_receipt', methods=['POST', 'GET'])
def print_receipt_route():

    receipt = Receipt(number = 28)

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
