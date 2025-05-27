def format_table_line(
    qty: int | str,
    desc: str,
    unit_price: float | str,
    subtotal: float | str,
    widths=(6, 23, 8, 8),
    is_header=False,
):
    """
    Formats a line of a table of 4 columns
    The total width of the paper is 45 chars
    """

    q_w, d_w, u_w, t_w = widths

    if is_header:
        return f"{str(qty):<{q_w}}{desc:<{d_w}}{unit_price:^{u_w}}{subtotal:>{t_w}}"
    else:
        desc = (desc[: d_w - 2] + "..") if len(desc) > d_w else desc
        return (
            f"{str(qty):<{q_w}}{desc:<{d_w}}{unit_price:^{u_w}.2f}{subtotal:>{t_w}.2f}"
        )


def format_totals_line(des: str, total: float, widths=(37, 8)):
    """
    Formats a line of a table of 2 columns
    The total width of the paper is 45 chars
    """
    d_w, t_w = widths
    return f"{des:>{d_w}}{total:>{t_w}.2f}"
