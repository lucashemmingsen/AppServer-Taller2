"""Product endpoints related tests"""
from unittest.mock import patch
import appserver.service.products_service


def test_get_products_without_token_returns_401_response(client):
    response = client.get('/products')
    assert response.status_code == 401


def test_get_products_with_invalid_token_returns_422_response(client, product_data):
    response = client.get('/products', headers=product_data.invalid_token_header(),
                          json=product_data.empty_json())
    assert response.status_code == 422


@patch.object(appserver.service.products_service.ProductsService, 'get_products')
def test_get_products_with_token_returns_200_response(get_products_mock, client, product_data):

    get_products_mock.return_value = product_data.get_products_return_value()
    response = client.get('/products', headers=product_data.valid_token_header(),
                          json=product_data.empty_json())
    assert response.status_code == 200


def test_get_product_without_token_returns_401_response(client):
    response = client.get('/products/512')
    assert response.status_code == 401


def test_add_product_without_token_returns_401_response(client):
    response = client.post('/products')
    assert response.status_code == 401


def test_add_product_if_body_not_json_400_response(client, product_data):
    response = client.post('/products', headers=product_data.valid_token_header())
    assert response.status_code == 400


def test_delete_product_without_token_401_response(client):
    pass


def test_delete_product_if_not_found_404_response(client, user_data, product_data):
    response = client.delete('/products/5bbe37a1e3c00f593839d19e', headers=product_data.valid_token_header())
    assert response.status_code == 404


def test_delete_product_if_invalid_product_id_400_response(client, user_data, product_data):
    response = client.delete('/products/5bbe37a3c00f593839d19e', headers=product_data.valid_token_header())
    assert response.status_code == 400


def test_delete_product_if_user_does_not_own_product_403_response(client, user_data, product_data):
    pass


def test_delete_product_200_response(client, user_data, product_data):
    pass


