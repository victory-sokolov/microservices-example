import json
import unittest

from project import create_app, db
from project.api.models import User
from project.tests.base import BaseTestCase
from utils import post_user_data

def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """ Tests for the Users Service. """

    def __init__(self, *args, **kwargs):
        self.app = create_app()
        self.app_test = self.app.test_client()
        super(TestUserService, self).__init__(*args, **kwargs)

    def test_users(self):
        """ Ensure the /ping route behaves correctly """
        response = self.app_test.get("/users/ping")

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """ Ensure new user can be added to database. """
        response = self.app_test.post(
            "/users",
            data=json.dumps(
                {"username": "viktor", "email": "viktorsokolov.and@gmail.com"}
            ),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("viktorsokolov.and@gmail.com was added", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """ Ensure error is throw if the JSON object is empty """
        response = self.app_test.post(
            "/users", data=json.dumps({}), content_type="application/json",
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid payload", data["message"])
        self.assertIn("fail", data["status"])

    def test_add_user_dublicate_email(self):
        """ Ensure error is thrown if the email already exists """
        response = post_user_data(self.app_test)
        response = post_user_data(self.app_test)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry. That email already exists.", data["message"])
        self.assertIn("fail", data["status"])

    def test_single_user(self):
        """ Ensure get single user behaves correctly. """
        user = User(username="viktor", email="viktorsokolov.and@gmail.com")
        db.session.add(user)
        db.session.commit()
        response = self.app_test.get(f"/users/{user.id}")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("viktor", data["data"]["username"])
        self.assertIn("viktorsokolov.and@gmail.com", data["data"]["email"])
        self.assertIn("success", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        add_user("viktor", "viktorsokolov.and@gmail.com")
        add_user("nick", "nick@gmail.com")
        response = self.app_test.get("/users")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]["users"]), 2)
        self.assertIn("viktor", data["data"]["users"][0]["username"])
        self.assertIn("viktorsokolov.and@gmail.com", data["data"]["users"][0]["email"])
        self.assertIn("nick", data["data"]["users"][1]["username"])
        self.assertIn("nick@gmail.com", data["data"]["users"][1]["email"])
        self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
