from unittest.mock import patch, MagicMock

# Checks if both printers are connected
def test_printers(client):
    with patch("app.Usb") as MockUsb, \
     patch("app.Network") as MockNetwork:

        mock_cashier = MagicMock()
        mock_kitchen = MagicMock()

        MockUsb.return_value = mock_cashier
        MockNetwork.return_value = mock_kitchen

        response = client.get('/check_printers')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == "ok"
        assert data['kitchen'] == "online"
        assert data['cashier'] == "online"

def test_printers_fail(client):
    response = client.get('/check_printers')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "not_connected"
