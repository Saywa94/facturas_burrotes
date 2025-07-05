# Facturas Burrotes

A Flask-based API for printing receipts and kitchen orders to thermal printers. This application is designed to be a simple backend service that can be integrated with a Point of Sale (POS) system.

## Features

*   Print receipts to a cashier printer.
*   Print orders to a kitchen printer.
*   Check the status of connected printers.
*   Support for both USB and Network printers.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd facturas_burrotes
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Printers:**
    Create a `.env` file in the root of the project to configure your printers. You can use the following template:

    ```env
    # For a USB printer, use the format: usb:VENDOR_ID:PRODUCT_ID
    # Example:
    # KITCHEN_PRINTER=usb:0x04b8:0x0e15
    # CASHIER_PRINTER=usb:0x0416:0x5011

    # For a network printer, use the format: network:IP_ADDRESS
    # Example:
    KITCHEN_PRINTER=network:192.168.1.101
    CASHIER_PRINTER=network:192.168.1.102
    ```

## Running the Application

To start the Flask development server, run the following command:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

The following endpoints are available:

*   `GET /`: A simple endpoint to check if the server is running.
*   `GET /check_printers`: Checks the connection status of both the kitchen and cashier printers.
    *   **Response:** `{"status": "ok"}` or `{"status": "not_connected", "offline_printer": "kitchen|cashier|both"}`
*   `POST /print_receipt`: Prints a receipt. Expects a JSON payload with the receipt data.
    *   **Response:** `{"status": "ok", "message": "Factura impresa exitosamente"}`
*   `POST /print_order`: Prints a kitchen order.
    *   **Response:** `{"status": "ok", "message": "Pedido impreso exitosamente"}`
*   `POST /test`: Sends a test print to the kitchen printer.
    *   **Response:** `{"status": "ok"}`

## Key Dependencies

*   [Flask](https://flask.palletsprojects.com/): The web framework used.
*   [python-escpos](https://github.com/python-escpos/python-escpos): A Python library to manipulate ESC/POS printers.
*   [python-dotenv](https://github.com/theskumar/python-dotenv): For managing environment variables.
