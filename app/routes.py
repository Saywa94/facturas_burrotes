from flask import Blueprint, request

from .receipts import validate_receipt
from .printers import check_both, print, test_print

from data.orders import order2

bp = Blueprint("main", __name__)


@bp.route("/")
def hello_world():
    return "Hello, Fusi!"


@bp.route("/test", methods=["POST", "GET"])
def test():
    test_print("kitchen")

    return {"status": "ok"}


@bp.route("/check_printers", methods=["GET"])
def check_printers():
    success, offline_printer = check_both()

    status = "ok" if success else "not_connected"
    return {"status": status, "offline_printer": offline_printer}


@bp.route("/print_receipt", methods=["POST", "GET"])
def print_receipt_route():
    receipt = validate_receipt(request.get_json())
    if receipt is None:
        return {"status": "error", "message": "Datos de factura incorrectos"}

    if not print("cashier", receipt):
        return {"status": "error", "message": "No se pudo imprimir la factura"}

    res = {"status": "ok", "message": "Factura impresa exitosamente"}
    return res


@bp.route("/print_order", methods=["POST", "GET"])
def print_order_route():
    order = order2

    if not print("kitchen", order):
        return {"status": "error", "message": "No se pudo imprimir el pedido"}

    res = {"status": "ok", "message": "Pedido impreso exitosamente"}
    return res
