from escpos.printer import Network, Usb
from escpos.exceptions import DeviceNotFoundError, USBNotFoundError
import logging

# Config constants
# Sould be in a config file or come from DB
wifi_printer_ip = "192.168.0.217"
usb_id_vendor = 0x0483
usb_id_product = 0x5743


def print_receipt():
    cashier = init_usb_printer(usb_id_vendor, usb_id_product)
    if (cashier == None):
        return False

    cashier.text("Fuck Yeah!!\n")
    cashier.text("This is a Caja REGISTRADORA!!!\n")
    cashier.qr("You can readme from your smartphone")
    cashier.text("QRRRR Bitches!!!!\n")
    cashier.cut()

    return True

def print_order():
    kitchen = init_wifi_printer(wifi_printer_ip) #Printer IP Address
    if (kitchen == None):
        return False
     
    kitchen.text("Fuck Yeah!!\n")
    kitchen.text("This is a test\n")
    kitchen.ln()
    kitchen.qr("You can readme from your smartphone")
    kitchen.cut()
    kitchen.text("QRRRR Bitches!!!!\n")
    kitchen.barcode('4006381333931','EAN13',64,2,'','')
    kitchen.cut()

    return True

def check_both():
    kitchen = init_wifi_printer(wifi_printer_ip) #Printer IP Address
    cashier = init_usb_printer(usb_id_vendor, usb_id_product)

    # Check if connected
    if (kitchen == None and cashier == None):
        return False, "both"
    if (kitchen == None):
        return False, "kitchen"
    if (cashier == None):
        return False, "cashier"

    # Check if online
    ok_kitchen = kitchen.is_online() 
    ok_cashier = cashier.is_online() 

    if (not ok_kitchen and not ok_cashier):
        return False, "both"
    if (not ok_kitchen):
        return False, "kitchen"
    if (not ok_cashier):
        return False, "cashier"

    return True, ""

def init_wifi_printer(ip, port=9100):
    try:
        printer = Network(ip, port=port, timeout=2)
        printer.set(align='center')
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
        printer.set(align='center') 
        return printer
    except USBNotFoundError:
        logging.error("USB printer not found. Check if it's connected and IDs are correct.")
    except OSError as e:
        logging.error(f"OS-level error initializing USB printer: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    
    return None
