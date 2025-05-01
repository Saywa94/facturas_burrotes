
def format_table_line(qty: int | str, desc: str, unit_price: float | str, subtotal: float | str, widths=(4, 16, 6, 6), is_header=False):

    q_w, d_w, u_w, t_w = widths

    if is_header:
        return f"{str(qty):<{q_w}}{desc:<{d_w}}{str(unit_price):>{u_w}}{str(subtotal):>{t_w}}"
    else:
        desc = (desc[:d_w - 1] + "…") if len(desc) > d_w else desc
        return f"{str(qty):<{q_w}}{desc:<{d_w}}{unit_price:>{u_w}.2f}{subtotal:>{t_w}.2f}"

