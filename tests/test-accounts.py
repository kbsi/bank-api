import pytest

def test_get_accounts(client):
    response = client.get('/api/accounts', headers={"Authorization": f"Bearer <JWT_TOKEN>"})
    assert response.status_code == 200

def test_create_account(client):
    response = client.post('/api/accounts', json={
        "balance": 500,
        "currency": "EUR"
    }, headers={"Authorization": f"Bearer <JWT_TOKEN>"})
    assert response.status_code == 201
