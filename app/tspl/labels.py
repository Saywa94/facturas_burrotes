from dataclasses import dataclass


@dataclass
class RestaurantLabel:
    product: str
    order_num: int
    proteins: str
    sauces: str
    sin_queso: bool = False

    def to_tspl(self) -> str:
        return "\r\n".join(
            [
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
                # if sin_queso show '-sin queso-'
                'TEXT 112,160,"3",0,1,1,"-sin queso-"' if self.sin_queso else "",
                # Print
                "PRINT 1,1",
                "",
            ]
        )
