from flask import Flask
from escpos.printer import Network, Usb
from escpos.exceptions import DeviceNotFoundError, USBNotFoundError
import logging

# Config constants
# Sould be in a config file or come from DB
# Printer IP Address
wifi_printer_ip = "192.168.0.217"
# USB printer IDs
usb_id_vendor = 0x0483
usb_id_product = 0x5743


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Fusi!'

@app.route('/check_printers', methods=['GET'])
def check_printers():
    kitchen = init_wifi_printer(wifi_printer_ip) #Printer IP Address
    if (kitchen == None):
        return {"status": "not_connected"}
    cashier = init_usb_printer(usb_id_vendor, usb_id_product)
    if (cashier == None):
        return {"status": "not_connected"}

    ok_kitchen = "online" if kitchen.is_online() else "offline"
    ok_cashier = "online" if cashier.is_online() else "offline"
    status = "ok" if ok_kitchen == "online" and ok_cashier == "online" else "offline"

    res = {
        "status": status,
        "kitchen": ok_kitchen,
        "cashier": ok_cashier
    }
    return res

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
        printer.set(align='center')  # Optional: basic test to ensure connection works
        return printer
    except USBNotFoundError:
        logging.error("USB printer not found. Check if it's connected and IDs are correct.")
    except OSError as e:
        logging.error(f"OS-level error initializing USB printer: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    
    return None

@app.route('/print', methods=['POST', 'GET'])
def print_factura():
    kitchen = Network("192.168.0.217") #Printer IP Address
    kitchen.text("Fuck Yeah!!\n")
    kitchen.text("This is a test\n")
    kitchen.ln()
    kitchen.qr("You can readme from your smartphone")
    kitchen.cut()
    kitchen.text("QRRRR Bitches!!!!\n")
    kitchen.barcode('4006381333931','EAN13',64,2,'','')
    kitchen.cut()

    # kitchen = Usb(0x0483, 0x5743) #Printer IP Address
    # kitchen.text("Fuck Yeah!!\n")
    # kitchen.text("This is a Caja REGISTRADORA!!!\n")
    # kitchen.qr("You can readme from your smartphone")
    # kitchen.text("QRRRR Bitches!!!!\n")
    # kitchen.cut()

    res = {
        "status": "ok",
        "message": "Factura impresa"
    }
    return res

if __name__ == "__main__":
    app.run(debug=True)

