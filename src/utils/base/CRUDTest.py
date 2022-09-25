from fastapi.testclient import TestClient
from main import app


class CRUDTest:
    endpoint_name: str
    object_schema: dict
    client = TestClient(app)

    def __init__(self, endpoint_name: str, object_schema: dict):
        self.endpoint_name = endpoint_name
        self.object_schema = object_schema

    def get(self, custom_response_value=None, expected_status=200):
        expected_response = custom_response_value or list(self.object_schema)
        response = self.client.get(self.endpoint_name)
        assert response.status_code == expected_status
        assert response.json() == expected_response
        return response

    def post(self, payload: any, custom_response_value=None, expected_status=200):
        expected_response = custom_response_value or self.object_schema
        response = self.client.post(self.endpoint_name, payload or self.object_schema)
        assert response.status_code == expected_status
        assert response.json() == expected_response
        return response

    def put(self, item_id: int, payload: any, custom_response_value=None, expected_status=200):
        expected_response = custom_response_value or self.object_schema
        response = self.client.put(self.endpoint_name + f"/{item_id}", payload or self.object_schema)
        assert response.status_code == expected_status
        assert response.json() == expected_response
        return response

    def delete(self, item_id: int, custom_response_value=None, expected_status=204):
        response = self.client.delete(self.endpoint_name + f"/{item_id}")
        assert response.status_code == expected_status
        if custom_response_value:
            assert response.json() == custom_response_value
        return response

    def get_one(self, item_id: int, custom_response_value=None, expected_status=200):
        expected_response = custom_response_value or self.object_schema
        response = self.client.delete(self.endpoint_name + f"/{item_id}")
        assert response.status_code == expected_status
        if custom_response_value:
            assert response.json() == expected_response
        return response
