from escpos.escpos import Escpos
from pydantic import BaseModel

class Receipt(BaseModel):
    number: int

def print_receipt(p: Escpos, receipt):
    try:

        p.text(f"{receipt.number}")
        p.ln
        p.text("This is a Caja REGISTRADORA!!!\n")
        p.qr("You can readme from your smartphone")
        p.text("QRRRR Bitches!!!!\n")
        p.cut()

        return True

    except:
        return False
