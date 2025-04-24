from typing import List, Optional
from pydantic import BaseModel, PositiveInt, model_validator

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
