from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
from flask import session


from user.models import User


class UserTest(unittest.TestCase):
    def create_app(self):
        self.db_name = "flaskbook_test"
        return create_app_base(
            MONGODB_SETTINGS={"DB": self.db_name},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="mySecret",
            )

    # Always have a setUp and tearDown
    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)
        
    def user_dict(self):
        return dict(
            first_name="Michael",
            last_name="Skolnik",
            username="michael",
            email="nunchuks@mailinator.com",
            password="test123",
            confirm="test123"
            )

    # Have to begin with test_
    def test_register_user(self):
        # Basic registration
        rv = self.app.post("/register/", data=self.user_dict(),
                           follow_redirects=True)
        assert User.objects.filter(username=self.user_dict()["username"]).count() == 1
        
        # Invalid username characters
        user2 = self.user_dict()
        user2["username"] = "test test"
        user2["email"] = "test@example.com"
        rv = self.app.post("/register/", data=user2, follow_redirects=True)
        assert "Invalid username" in str(rv.data)
        
        # Is username being saved in lowercase
        user3 = self.user_dict()
        user3["username"] = "TestUser"
        user3["email"] = "test2@example.com"
        rv = self.app.post("/register/", data=user3, follow_redirects=True)
        assert User.objects.filter(username=user3["username"].lower()).count() == 1

    def test_login_user(self):
        # Create user
        self.app.post("/register/", data=self.user_dict())
        # Login user
        rv = self.app.post("/login/", data=dict(
            username=self.user_dict()["username"],
            password=self.user_dict()["password"]
            ))
        # Check the session is set
        with self.app as c:
            rv = c.get("/")
            assert session.get("username") == self.user_dict()["username"]
        
        rv = self.app.post("/login/", data=dict(
            username=self.user_dict()["username"],
            password="test"
            ))
        assert "Incorrect credentials" in str(rv.data)
        
        rv = self.app.post("/login/", data=dict(
            username="juan",
            password=self.user_dict()["password"]
            ))
        assert "Incorrect credentials" in str(rv.data)

    def test_edit_profile(self):
        # Create a user
        self.app.post("/register/", data=self.user_dict())
        # Login the user
        rv = self.app.post("/login/", data=dict(
            username=self.user_dict()["username"],
            password=self.user_dict()["password"]
            ))
        # Check that user has Edit button on own profile
        rv = self.app.get("/" + self.user_dict()["username"] + "/")
        assert "Edit Profile" in str(rv.data)
        
        # Edit fields
        user = self.user_dict()
        user["first_name"] = "Test First"
        user["last_name"] = "Test Last"
        user["username"] = "TestUsername"
        user["email"] = "Test@example.com"
        
        # Edit the user
        rv = self.app.post("/edit/", data=user)
        assert "Profile updated" in str(rv.data)
        edited_user = User.objects.first()
        assert edited_user.first_name == "Test First"
        assert edited_user.last_name == "Test Last"
        assert edited_user.username == "testusername"
        assert edited_user.email == "test@example.com"

        # Create a second user
        self.app.post("/register/", data=self.user_dict())
        # Login the user
        rv = self.app.post("/login/", data=dict(
            username=self.user_dict()["username"],
            password=self.user_dict()["password"]
            ))
            
        # Try to save same email
        user = self.user_dict()
        user["email"] = "test@example.com"
        rv = self.app.post("/edit/", data=user)
        assert "Email already exists" in str(rv.data)
        
        # Try to save same username
        user = self.user_dict()
        user["username"] = "TestUsername"
        rv = self.app.post("/edit/", data=user)
        assert "Username already exists" in str(rv.data)
