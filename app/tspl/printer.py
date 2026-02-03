import logging
import socket

from app.tspl.exceptions import (
    TSPLException,
    TSPLTimeoutError,
    TSPLConnectionError,
    TSPLPrinterError,
)
from app.tspl.labels import LabelsRequest, build_labels_payload


class TSPLPrinter:
    def __init__(
        self, printer_id: str, ip: str, port: int = 9100, timeout: float = 3.0
    ):
        self.printer_id = printer_id
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def send_raw(self, payload: bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            s.connect((self.ip, self.port))
            s.sendall(payload)

    def check_ready(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((self.ip, self.port))
        except socket.timeout:
            raise TSPLTimeoutError()
        except OSError as e:
            raise TSPLConnectionError(str(e))

    def print(self, payload: str):
        try:
            self.send_raw(payload.encode("latin-1"))
        except socket.timeout:
            raise TSPLTimeoutError("Printer did not respond in time.")
        except OSError as e:
            raise TSPLConnectionError(str(e))

    def is_available(self) -> bool:
        try:
            self.check_ready()
            return True
        except TSPLPrinterError:
            return False


def print_labels(labels_req: LabelsRequest) -> bool:
    printer = TSPLPrinter(
        printer_id="tspl_label_1",
        ip="192.168.0.94",
    )

    try:
        payload = build_labels_payload(labels_req.labels)
        printer.print(payload)
        return True
    except TSPLException as e:
        logging.exception(e)
        return False
