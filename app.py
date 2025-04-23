from flask import Flask
from escpos.printer import Network, Usb

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Fusi!'

@app.route('/printers', methods=['GET'])
def printers():
    printers = getPrinters()
    res = {
        "status": "ok",
        "message": "Printers list",
        "printers": printers
    }
    return res

@app.route('/print', methods=['POST', 'GET'])
def print_factura():
    # kitchen = Network("192.168.0.217") #Printer IP Address
    # kitchen.text("Fuck Yeah!!\n")
    # kitchen.text("This is a test\n")
    # kitchen.qr("You can readme from your smartphone")
    # kitchen.cut()
    # kitchen.text("QRRRR Bitches!!!!\n")
    # kitchen.barcode('4006381333931','EAN13',64,2,'','')
    # kitchen.cut()

    kitchen = Usb(0x0483, 0x5743) #Printer IP Address
    kitchen.text("Fuck Yeah!!\n")
    kitchen.text("This is a Caja REGISTRADORA!!!\n")
    kitchen.qr("You can readme from your smartphone")
    kitchen.text("QRRRR Bitches!!!!\n")
    kitchen.cut()

    res = {
        "status": "ok",
        "message": "Factura impresa"
    }
    return res

if __name__ == "__main__":
    app.run(debug=True)

def getPrinters():
    # TODO: get printer list
    return ["Printer 1", "Printer 2"]
