from escpos.printer import Network, Usb
from escpos.exceptions import DeviceNotFoundError, USBNotFoundError
from typing import Literal, overload
import logging
import time

from flask import current_app

from .orders import Order, print_order
from .receipts import Receipt, print_receipt


def test_print(
    printer_location: Literal["kitchen", "cashier"],
):
    printer_type = current_app.config[f"{printer_location.upper()}_PRINTER_TYPE"]
    printer_addr = current_app.config[f"{printer_location.upper()}_PRINTER_ADDR"]

    p = retry_get_printer(printer_type, printer_addr)
    if p is None:
        logging.error(f"Failed to connect to {printer_location} printer after retries.")
        return False

    # TEST AREA

    p.set(bold=True, align="center", custom_size=True, height=2, width=2)

    p.ln()

    p.textln("620466028")
    p.ln()
    p.textln("GRUPO GFV S.R.L.")

    p.ln()

    p.cut()

    return None


# General printer function
@overload
def print(printer_location: Literal["kitchen"], data: Order) -> bool: ...
@overload
def print(printer_location: Literal["cashier"], data: Receipt) -> bool: ...


def print(printer_location: Literal["kitchen", "cashier"], data: Order | Receipt):
    printer_type = current_app.config[f"{printer_location.upper()}_PRINTER_TYPE"]
    printer_addr = current_app.config[f"{printer_location.upper()}_PRINTER_ADDR"]

    printer = retry_get_printer(printer_type, printer_addr)
    if printer is None:
        logging.error(f"Failed to connect to {printer_location} printer after retries.")
        return False

    # NOTE: Add here other printer locations
    if printer_location == "kitchen":
        assert isinstance(data, Order)
        return print_order(printer, order=data)
    elif printer_location == "cashier":
        assert isinstance(data, Receipt)
        return print_receipt(printer, receipt=data)


def get_printer(
    printer_type: Literal["usb", "network"], printer_addr: tuple[int, int] | str
):
    """
    Initializes a printer by printer type
    NOTE: Add here other printer types
    """

    if printer_type == "usb":
        return init_usb_printer(printer_addr[0], printer_addr[1])
    elif printer_type == "network":
        return init_wifi_printer(printer_addr)


def retry_get_printer(printer_type, printer_addr, retries=3, delay=1):
    for attempt in range(retries):
        try:
            printer = get_printer(printer_type, printer_addr)
            if printer:
                return printer
        except Exception as e:
            logging.error(f"[Retry {attempt + 1}] Printer connection failed: {e}")
        time.sleep(delay)
    return None


def check_both():
    kitchen_printer_type = current_app.config["KITCHEN_PRINTER_TYPE"]
    kitchen_printer_addr = current_app.config["KITCHEN_PRINTER_ADDR"]

    kitchen = get_printer(kitchen_printer_type, kitchen_printer_addr)

    cashier_printer_type = current_app.config["CASHIER_PRINTER_TYPE"]
    cashier_printer_addr = current_app.config["CASHIER_PRINTER_ADDR"]

    cashier = get_printer(cashier_printer_type, cashier_printer_addr)

    # Check if connected
    if kitchen is None and cashier is None:
        return False, "both"
    if kitchen is None:
        return False, "kitchen"
    if cashier is None:
        return False, "cashier"

    # Check if online
    ok_kitchen = kitchen.is_online()
    ok_cashier = cashier.is_online()

    if not ok_kitchen and not ok_cashier:
        return False, "both"
    if not ok_kitchen:
        return False, "kitchen"
    if not ok_cashier:
        return False, "cashier"

    return True, ""


def init_wifi_printer(ip, port=9100):
    try:
        printer = Network(ip, port=port, timeout=5)
        printer.set(align="center")
        return printer
    except DeviceNotFoundError as e:
        logging.error(f"ESC/POS device not found error: {e}")
    except OSError as e:
        logging.error(f"OS error during printer initialization: {e}")
    except Exception as e:
        logging.error(f"Unexpected error initializing printer: {e}")

    return None


def init_usb_printer(id_vendor, id_product):
    try:
        printer = Usb(id_vendor, id_product)
        printer.set(align="center")
        return printer
    except USBNotFoundError:
        logging.error(
            "USB printer not found. Check if it's connected and IDs are correct."
        )
    except OSError as e:
        logging.error(f"OS-level error initializing USB printer: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None
