from dataclasses import dataclass
import logging
from typing import List

from pydantic import BaseModel, PositiveInt
from pydantic_core import ValidationError


class LabelRequest(BaseModel):
    product: str
    order_num: PositiveInt
    proteins: str
    sauces: str
    sin_queso: bool


def validate_label_request(data) -> LabelRequest | None:
    try:
        LabelRequest.model_validate(data)
    except ValidationError as e:
        logging.error(e)
        return None


class LabelsRequest(BaseModel):
    labels: List[LabelRequest]


def validate_labels(data) -> LabelsRequest | None:
    try:
        return LabelsRequest.model_validate(data)
    except ValidationError as e:
        logging.error(e)
        return None


@dataclass
class RestaurantLabel:
    product: str
    order_num: int
    proteins: str
    sauces: str
    sin_queso: bool = False

    def to_tspl(self) -> str:
        commands = [
            # Label setup
            "SIZE 50 mm, 25 mm",
            "GAP 3 mm, 0",
            "DIRECTION 1",
            "CLS",
            # Top line: product name (top left) and order number (top right)
            f'TEXT 20,20,"4",0,1,1,"{self.product}"',
            f'TEXT 340,20,"4",0,1,1,"{self.order_num}"',
            # Proteins
            f'TEXT 20,80,"3",0,1,1,"{self.proteins}"',
            # Sauces
            f'TEXT 20,120,"3",0,1,1,"{self.sauces}"',
        ]

        # if sin_queso show '-sin queso-'
        if self.sin_queso:
            commands.append('TEXT 112,160,"3",0,1,1,"-sin queso-"')

        # Print command
        commands.extend(["PRINT 1,1", ""])

        return "\r\n".join(commands)


def build_labels_payload(labels: list[LabelRequest]) -> str:
    parts: list[str] = []

    for label_req in labels:
        label = RestaurantLabel(
            product=label_req.product,
            order_num=label_req.order_num,
            proteins=label_req.proteins,
            sauces=label_req.sauces,
            sin_queso=label_req.sin_queso,
        )

        parts.append(label.to_tspl())

    return "\r\n".join(parts)
