from flask import Blueprint, request

from app.tspl.exceptions import TSPLException
from app.tspl.labels import RestaurantLabel, validate_labels
from app.tspl.printer import TSPLPrinter, print_labels
from app.orders import validate_order

from .receipts import validate_receipt
from .printers import check_both, print, test_print


bp = Blueprint("main", __name__)


@bp.route("/")
def hello_world():
    return "Hello, Fusi!"


@bp.route("/test_printers", methods=["POST", "GET"])
def test():
    if not test_print("cashier"):
        return {"status": "error", "message": "Cashier printer not working"}
    if not test_print("kitchen"):
        return {"status": "error", "message": "Kitchen printer not working"}

    res = {"status": "ok", "message": "Printers working correctly"}
    return res


@bp.route("/test_tspl", methods=["POST", "GET"])
def test_tspl():
    printer = TSPLPrinter(printer_id="tspl_label_1", ip="192.168.0.94")
    label = RestaurantLabel(
        product="Burro L",
        order_num=66,
        proteins="Pollo",
        sauces="Ajosa",
    )
    payload = label.to_tspl()

    try:
        printer.print(payload)
        return {"status": "ok", "message": "TSPL printer reachable"}
    except TSPLException as e:
        return {"status": "error", "message": str(e)}


@bp.route("/check_printers", methods=["GET"])
def check_printers():
    success, offline_printer = check_both()

    status = "ok" if success else "not_connected"
    return {"status": status, "offline_printer": offline_printer}


@bp.route("/print_receipt", methods=["POST"])
def print_receipt_route():
    receipt = validate_receipt(request.get_json())
    if receipt is None:
        return {"status": "error", "message": "Datos de factura incorrectos"}

    if not print("cashier", receipt):
        return {"status": "error", "message": "No se pudo imprimir la factura"}

    res = {"status": "ok", "message": "Factura impresa exitosamente"}
    return res


@bp.route("/print_order", methods=["POST"])
def print_order_route():
    order = validate_order(request.get_json())
    if order is None:
        return {"status": "error", "message": "Datos de pedido incorrectos"}

    if not print("kitchen", order):
        return {"status": "error", "message": "No se pudo imprimir el pedido"}

    res = {"status": "ok", "message": "Pedido impreso exitosamente"}
    return res


@bp.route("/print_labels", methods=["POST", "GET"])
def print_labels_route():
    labels_req = validate_labels(request.get_json())
    if labels_req is None or not labels_req.labels:
        return {"status": "error", "message": "Datos de etiquetas incorrectos"}
    # labels_req = LabelsRequest(
    #     labels=[
    #         Label(
    #             product="Burro M",
    #             order_num=66,
    #             proteins="Pollo",
    #             sauces="Italiana, Spicy",
    #             sin_queso=False,
    #         ),
    #         Label(
    #             product="Bowl XL",
    #             order_num=66,
    #             proteins="Pollo, Res, Chorizo",
    #             sauces="Ajosa, Curry",
    #             sin_queso=False,
    #         ),
    #     ]
    # )

    if not print_labels(labels_req):
        return {"status": "error", "message": "No se pudo imprimir la etiqueta"}

    return {"status": "ok", "message": f"{len(labels_req.labels)} etiquetas impresas"}
