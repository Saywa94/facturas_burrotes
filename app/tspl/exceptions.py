class TSPLException(Exception):
    """Base class for all TSPL-related errors."""

    pass


class TSPLConnectionError(TSPLException):
    """Could not connect to the printer."""

    pass


class TSPLTimeoutError(TSPLException):
    """Printer did not respond in time."""

    pass


class TSPLPrinterError(TSPLException):
    """
    Printer reported an error state (paper out, cover open, etc).
    """

    def __init__(self, status_byte: bytes):
        self.status_byte = status_byte
        super().__init__(f"Printer error status: {status_byte!r}")
