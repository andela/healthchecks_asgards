from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        ### Assert the expected status code and check's status
        self.assertEquals(r.status_code, 200)
        self.assertEquals(check.status, "up")

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 400)

        ### Test that it only allows post requests

    def test_only_allows_post_requests(self):
        # random generated UUID
        check_code = '04dd700e-21f5-4e1b-a7ae-feb8721b708b'
        url = "/api/v1/checks/%s/pause" % check_code

        # Trying GET request
        r = self.client.get(url, HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 405)
