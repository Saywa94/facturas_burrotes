import logging
from typing import List, Optional
from pydantic import BaseModel, PositiveInt, model_validator
from escpos.escpos import Escpos

class OrderItem(BaseModel):
    quantity: PositiveInt
    product: str
    details: Optional[str]
    extra: Optional[str]
    is_cooked: bool

class Order(BaseModel):
    number: int
    customer: Optional[str]
    date_time: str
    dine_in: List[OrderItem]
    take_out: List[OrderItem]
    beeper: Optional[int]
    comment: Optional[str]

    @model_validator(mode="after")
    def validate_beeper_for_dine_in(self) -> 'Order':
        if self.dine_in and self.beeper is None:
            raise ValueError("Beeper is required when dine_in is not empty.")
        return self

def print_order(p: Escpos, order: Order):
    """
    Prints a formatted order receipt.
    Returns True on success and False on failure.
    """
     
    try:
        p.ln(3)
        # Print Big Order number
        p.set(bold=True, align="center", custom_size=True, height=2, width=2)
        p.textln(f"{order.number}")
        p.ln(2)

        # If there is a customer name
        if order.customer:
            p.set(align="left", custom_size=True, height=2, width=1)
            p.textln(f"Cliente: {order.customer}")

        # Date time
        p.set(bold=False, align="left", custom_size=True, height=1, width=1)
        p.textln(f"{order.date_time}\n")

        # Dine In
        if order.dine_in:
            print_order_items(p, order.dine_in, "En Local", beeper=order.beeper)

        # Take Out
        if order.take_out:
            print_order_items(p, order.take_out, "Para Llevar")

        # Comments
        if order.comment:
            p.ln()
            p.set(align="left", bold=True)
            p.textln("Comentario:")
            p.set(bold=False)
            p.textln(order.comment)

        p.ln()

        p.cut()

        return True
    except Exception as e:
        logging.exception(f"Error printing order: {e}")
        return False

def print_order_items(p: Escpos, items: List[OrderItem], header: str, beeper: Optional[int] = None):
    p.set(align='center', custom_size=True, height=2, width=1)
    p.textln(header)

    if beeper is not None:
        p.set(align='center', custom_size=True, height=1, width=1)
        p.textln(f"beeper - {beeper}")

    p.textln('-' * 32)

    sorted_items = sorted(items, key=lambda x: not x.is_cooked)
    is_cooked = sorted_items[0].is_cooked

    for item in sorted_items:
        if item.is_cooked != is_cooked:
            p.textln('*' * 6)
            is_cooked = item.is_cooked

        p.set(bold=True, align="left", custom_size=True, height=2, width=1)
        p.ln()
        p.text(f"x{item.quantity} - {item.product}")

        p.set(bold=False, custom_size=True, height=1, width=1)
        if item.details:
            p.ln()
            p.textln('   ' + item.details)
        if item.extra:
            p.ln()
            p.textln('   ' + item.extra)

