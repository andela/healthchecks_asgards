import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase
from django.test import Client


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()
        self.client = Client()
        self.channel = Channel()

    def post(self, data, expected_error=None):
        response = self.client.post(self.URL, json.dumps(data),
                                    content_type="application/json")

        if expected_error:
            self.assertEqual(response.status_code, 400)

            ### Assert that the expected error is the response error
            self.assertEqual(response.json()["error"], expected_error)

        return response

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

        ### Assert the expected last_ping and n_pings values
        self.assertEqual(check.last_ping, None)
        self.assertEqual(check.n_pings, 0)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        response = self.client.post(
            self.URL,
            payload,
            HTTP_X_API_KEY="abc",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response

        self.post(data={}, expected_error="wrong api_key")

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type

        data = "Invalid json"

        response = self.client.post(self.URL, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    ### Test for the assignment of channels
    def test_it_assigns_channels(self):
        # create a channel that belongs to alice
        channel = Channel(user=self.alice)
        channel.save()

        # create a check via api
        data = {
            "api_key": "abc",
            "name": "Test",
            "channels": "*"
        }

        response = self.post(data)
        self.assertEqual(response.status_code, 201)
        # Assert the new check has alice's channel
        self.assertEqual(Check.objects.get(name="Test").user, channel.user)


    ### Test for the 'timeout is too small' and 'timeout is too large' errors
    def tests_it_handles_invalid_time_outs(self):
        data = {"api_key": "abc", "timeout": 604810}
        self.post(data, expected_error="timeout is too large")

        data = {"api_key": "abc", "timeout": 0}
        self.post(data, expected_error="timeout is too small")
