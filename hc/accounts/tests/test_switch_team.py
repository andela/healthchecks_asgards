from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)

        ### Assert the contents of r
        """
        Since r contains the url and this url has the name of the alice.
        then name of alice must be in the url
        """
        self.assertContains(r,"This belongs to Alice")


    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url)
        ### Assert the expected error code
        """
        The url will raise a 403 error because the team leader {alice}
        has not been set. 
        Forbidden error, The client cannot access that url  because 
        charlie is not in alice team.
        """

        self.assertEqual(r.status_code, 403)

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        ### Assert the expected error code
        """
        it switches to the team created by alice.
        The code is 200 mean ok, the server answered the request successfully.
        """
        self.assertEqual(r.status_code, 200)
