import os

from fastapi.testclient import TestClient
from unittest import TestCase
from moto import mock_aws

from app.main import app
from app.models.event import Event

client = TestClient(app)


@mock_aws(config={"dynamodb": {}})
class TestEndpoints(TestCase):
    def setUp(self):
        os.environ["EVENTS_TABLE"] = "EventsTable"
        os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"

        Event.create_table()

    def test_create_event_success(self):
        valid_event_request = {
            "id": "123",
            "type": "test",
            "payload": {"key": "value"},
        }

        response = client.post("/events", json=valid_event_request)
        response_body = response.json()

        self.assertEqual(201, response.status_code)
        self.assertEqual(valid_event_request["id"], response_body["id"])

    def test_create_event_missing_id(self):
        invalid_event_request = {
            "type": "test",
            "payload": {"key": "value"},
        }

        response = client.post("/events", json=invalid_event_request)
        response_body = response.json()

        self.assertEqual(422, response.status_code)
        self.assertIn("id", response_body["detail"][0]["loc"])

    def test_get_event_success(self):
        valid_event_request = {
            "id": "456",
            "type": "test",
            "payload": {"key": "value"},
        }
        client.post("/events", json=valid_event_request)

        response = client.get("/events/456")

        self.assertEqual(200, response.status_code)
        self.assertEqual("456", response.json()["id"])

    def test_get_event_not_found(self):
        response = client.get("/events/789")

        self.assertEqual(404, response.status_code)
