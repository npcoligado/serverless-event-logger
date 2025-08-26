from unittest import TestCase

from moto import mock_aws



@mock_aws
class TestEndpoints(TestCase):
    def test_create_event_success(self): ...

    def test_create_event_missing_id(self): ...
