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
            p.set(align='center', custom_size=True, height=2, width=1)
            p.textln('En Local')

            p.set(align='center', custom_size=True, height=1, width=1)
            p.textln(f"beeper - {order.beeper}")
            p.textln('-' * 32)

            # TODO: Filter by order.is_cooked
            for item in order.dine_in:
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


        # TODO: Take Out

        # TODO: Comments

        p.ln()


        p.cut()

        return True
    except:
        return False
