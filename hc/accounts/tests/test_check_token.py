from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        # The profile token is a harsh value created with the make_password.
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    """
    First we set the username and password of alice
    because alice was already logged in. NB{ should not be logged out.}
    and the post to check it redirects to /checks/
    """
    def test_redirect_already_logged_in_clients(self):
        self.client.login(username = "alice@example.org", password = "password")

        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")


    ### Login with a bad token and check that it redirects
    """
    Check the url is not valid.
    This happens when the secret token in the url is not the correct one.
    """
    def test_bad_token_passed(self):
        #Change url to have an invalid token.
        url = "/accounts/check_token/alice/incorrect-token/"
        r = self.client.post(url)
        self.assertNotEqual(url,"/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/accounts/login/")


