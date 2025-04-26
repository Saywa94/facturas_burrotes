import os
from dotenv import load_dotenv

load_dotenv()

def parse_printer(value):
    """
    Parses a printer string like 'usb:0x1234:0x5678' or 'network:192.168.1.100'
    Returns a tuple: (type, address_or_ids)
    """
    if not value:
        return None, None

    parts = value.split(":", 1)
    if len(parts) != 2:
        return None, None

    ptype = parts[0]
    payload = parts[1]

    if ptype == "usb":
        try:
            vid, pid = map(lambda x: int(x, 16), payload.split(":"))
            return ptype, (vid, pid)
        except ValueError:
            return None, None
    elif ptype == "network":
        return ptype, payload
    else:
        return None, None


class BaseConfig:
    KITCHEN_PRINTER_TYPE, KITCHEN_PRINTER_ADDR = parse_printer(os.getenv("KITCHEN_PRINTER"))
    CASHIER_PRINTER_TYPE, CASHIER_PRINTER_ADDR = parse_printer(os.getenv("CASHIER_PRINTER"))
