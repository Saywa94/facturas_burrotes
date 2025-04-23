def test_printers(client):
    response = client.get('/printers')

    assert response.status_code == 200
    data = response.get_json()
    assert 'printers' in data

    assert len(data['printers']) >= 2

    assert True
