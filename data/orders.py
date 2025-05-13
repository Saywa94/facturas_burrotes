from app.orders import Order, OrderItem

order1 = Order(
    number = 28,
    customer = None,
    date_time = "24/04/2025 - 19:30:25",
    dine_in = [
        OrderItem(
            quantity=1,
            product="Burro M - Pollo",
            details = "Queso, Mayo, Spicy", 
            extra = None,
            is_cooked=True
        ),
        OrderItem(quantity=1, product="Bowl L - Carne, Chori", details = "Queso, Curry, Ketchup, Burguer", extra = None, is_cooked=True),
        OrderItem(
            quantity=2,
            product="CocaCola 500ml",
            details = None, 
            extra = None,
            is_cooked=False
        ),
    ],
    take_out = [
        OrderItem(
            quantity=1,
            product="Burro M - Pollo",
            details = "Queso, Mayo, Spicy", 
            extra = None,
            is_cooked=True
        ),
        OrderItem(quantity=1, product="Bowl L - Carne, Chori", details = "Queso, Curry, Ketchup, Burguer", extra = None, is_cooked=True),
        OrderItem(
            quantity=2,
            product="CocaCola 500ml",
            details = None, 
            extra = None,
            is_cooked=False
        ),
    ],
    beeper = 8,
    comment = "Poquito picante porfavor"
)

order2 = Order(
    number = 43,
    customer = None,
    date_time = "24/04/2025 - 19:30:25",
    dine_in = [],
    beeper = None,
    comment = None,
    take_out = [
        OrderItem(
            quantity=1,
            product="Burro XL - Pollo, Carne, Chori",
            details = "Mayo, Spicy", 
            extra = None,
            is_cooked=True
        ),
        OrderItem(quantity=1, product="Bowl L - Carne, Chori", details = "Curry, Ketchup, Burguer", extra = None, is_cooked=True),
        OrderItem(quantity=2, product="Burro M - Pollo", details = "Curry, Spicy", extra = "- Sin Queso -", is_cooked=True),
        OrderItem(
            quantity=2,
            product="CocaCola 500ml",
            details = None, 
            extra = None,
            is_cooked=False
        ),
        OrderItem(
            quantity=1,
            product="Fanta 300ml",
            details = None, 
            extra = None,
            is_cooked=False
        ),
    ],
)
