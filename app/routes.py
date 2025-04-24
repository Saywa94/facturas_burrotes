from flask import Blueprint
from .printers import check_both, print_order,print_receipt

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
    if not print_receipt():
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
    if not print_order():
        return {
            "status": "error",
            "message": "No se pudo imprimir el pedido"
        }

    res = {
        "status": "ok",
        "message": "Pedido impreso exitosamente"
    }
    return res
