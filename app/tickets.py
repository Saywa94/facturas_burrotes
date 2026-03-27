from typing import Optional
from uuid import UUID
from escpos.escpos import Escpos
from pydantic import BaseModel, ValidationError
import logging

from app.assets import LOGO_IMAGE
from app.config import BASE_URL


class TicketPayload(BaseModel):
    numero_factura: int
    numero_delivery: Optional[str]  # nullable CharField in Django
    branch: str
    phone_number: str
    total: float
    date: str  # "DD/MM/YYYY - HH:MM:SS"
    public_id: UUID
    verification_code: str


class TicketWrapper(BaseModel):
    ticket_payload: TicketPayload


def validate_ticket(data) -> TicketPayload | None:
    try:
        return TicketWrapper.model_validate(data).ticket_payload
    except ValidationError as e:
        logging.error(e)
        return None


BIG_CENTER = {
    "font": "a",
    "bold": True,
    "align": "center",
    "custom_size": True,
    "height": 2,
    "width": 2,
}
NORMAL = {
    "font": "a",
    "bold": False,
    "align": "center",
    "custom_size": True,
    "height": 1,
    "width": 1,
}
SMALL_CENTER = {
    "font": "b",
    "bold": False,
    "align": "center",
    "custom_size": True,
    "height": 1,
    "width": 1,
}


def print_ticket(p: Escpos, ticket: TicketPayload):
    try:
        p.set(**BIG_CENTER)
        # Print order number (first 2 digits)
        p.textln(f"{ticket.numero_factura % 100:02d}")
        if ticket.numero_delivery:
            p.ln(1)
            p.textln(f"PedidosYa: #{ticket.numero_delivery}")
        p.ln(1)

        p.set(**NORMAL)
        p.image(
            img_source=LOGO_IMAGE,
            center=True,
        )
        p.ln()

        p.textln(f"Sucursal: {ticket.branch}")
        p.textln(f"Whatsapp: {ticket.phone_number}")
        p.textln(f" Monto total: {int(ticket.total)} Bs.")

        p.textln(ticket.date)

        p.set(**SMALL_CENTER)
        p.ln()
        p.textln("Consulte los detalles de su pedido:")

        p.qr(
            content=f"{BASE_URL}/orden/{ticket.public_id}",
            size=5,
            center=True,
        )

        p.set(**BIG_CENTER)
        p.textln(" ".join(ticket.verification_code))

        p.cut()

        return True

    except Exception as e:
        logging.exception(f"Error printing order: {e}")
        return False
    finally:
        p.close()
