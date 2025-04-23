from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Fusi!'

@app.route('/print', methods=['POST', 'GET'])
def print_factura():
    res = {
        "status": "ok",
        "message": "Factura impresa"
    }
    return res

if __name__ == "__main__":
    app.run(debug=True)
