from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302

        ### Assert that a user was created
<<<<<<< HEAD
        """ @marvin : 
        Create new instance of User 
        and check that it is authenticated. 
        https://docs.djangoproject.com/en/1.10/ref/contrib/auth/
        """
        self.alice = User(username="alice", email="alice@example.org")
        self.alice.set_password("password")
        self.alice.save()

        self.assertTrue(self.alice.is_authenticated)
=======
        self.assertEqual(User.objects.count(), 1)
>>>>>>> 8da8db087f343178d78cb4ea81d2f083bee78f9d

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        ### Assert contents of the email body
<<<<<<< HEAD
        
        """ @marvin : 
        Call the send_mail function that's in the Mail module.
        https://docs.djangoproject.com/en/1.10/ref/contrib/auth/
        """
        
        self.assertNotIn(mail.outbox[0].subject,[None,""],msg = "Subject should not be empty.") 
        self.assertNotIn(mail.outbox[0].from_email,[None,""],msg = "Invalid format of the sender email address.")
        
        print mail.outbox[0].recipient_list

        #self.assertNotEqual(len(mail.outbox[0].recipient_list), 0)
        #self.assertNotIn(mail.outbox[0].from_email, mail.outbox[0].recipient_list, msg = "Should not send yourself a copy of the client data.")
=======
        self.AssertEqual(mail.outbox[0].body, 'Hi go check out this link healthchecks.io')

>>>>>>> 8da8db087f343178d78cb4ea81d2f083bee78f9d

        ### Assert that check is associated with the new user
        re_check = Check.objects.get(code=check.code)
        assert re_check.user

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ### Any other tests?

