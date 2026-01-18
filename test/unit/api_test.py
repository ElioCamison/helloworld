import pytest

from app.api import api_application


@pytest.mark.unit
class TestApi:

    def setup_method(self):
        self.client = api_application.test_client()

    def test_hello_endpoint(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert b"Hello from The Calculator!" in response.data

    def test_add_ok(self):
        response = self.client.get("/calc/add/2/3")
        assert response.status_code == 200
        assert response.data == b"5"

    def test_add_type_error(self):
        response = self.client.get("/calc/add/a/3")
        assert response.status_code == 400

    def test_substract_ok(self):
        response = self.client.get("/calc/substract/5/2")
        assert response.status_code == 200
        assert response.data == b"3"

    def test_substract_type_error(self):
        response = self.client.get("/calc/substract/a/2")
        assert response.status_code == 400
