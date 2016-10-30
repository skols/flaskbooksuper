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
        
        # Confirm the user
        user = User.objects.get(username=self.user_dict()["username"])
        code = user.change_configuration.get("confirmation_code")
        rv = self.app.get("/confirm/" + user.username + "/" + code + "/")
        assert "Your email has been confirmed" in str(rv.data)
        
        # Try again to confirm
        rv = self.app.get("/confirm/" + user.username + "/" + code + "/")
        assert rv.status_code == 404
        
        # Check change configuration is empty
        user = User.objects.get(username=self.user_dict()["username"])
        assert user.change_configuration == {}

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
        
        # Confirm the user
        user = User.objects.get(username=self.user_dict()["username"])
        code = user.change_configuration.get("confirmation_code")
        rv = self.app.get("/confirm/" + user.username + "/" + code + "/")
        
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
        
        # Edit the user
        rv = self.app.post("/edit/", data=user)
        assert "Profile updated" in str(rv.data)
        edited_user = User.objects.first()
        assert edited_user.first_name == "Test First"
        assert edited_user.last_name == "Test Last"
        assert edited_user.username == "testusername"
        # assert edited_user.email == "test@example.com"
        
        # Check new email is in change configuration
        user["email"] = "test@example.com"
        rv = self.app.post("/edit/", data=user)
        test_message = "You will need to confirm the new email address \
                               to complete this change."
        assert test_message in str(rv.data)
        db_user = User.objects.first()
        code = db_user.change_configuration.get("confirmation_code")
        new_email = db_user.change_configuration.get("new_email")
        assert new_email == user["email"]
        
        # Now confirm
        rv = self.app.get("/confirm/" + db_user.username + "/" + code + "/")
        db_user = User.objects.first()
        assert db_user.email == user["email"]
        assert db_user.change_configuration == {}

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

    def test_get_profile(self):
        # Create a user
        self.app.post("/register/", data=self.user_dict())
        
        # Get the user's profile
        rv = self.app.get("/" + self.user_dict()["username"] + "/")
        assert self.user_dict()["username"] in str(rv.data)
        
        # Get a 404
        rv = self.app.get("/noexist/")
        assert rv.status_code == 404

    def test_forgot_password(self):
        # Create a user
        self.app.post("/register/", data=self.user_dict())
        
        # Confirm the user
        user = User.objects.get(username=self.user_dict()["username"])
        code = user.change_configuration.get("confirmation_code")
        rv = self.app.get("/confirm/" + user.username + "/" + code + "/")
        
        # Enter user forgot email
        rv = self.app.post("/forgot/",
                            data=dict(email=self.user_dict().get("email")))
        user = User.objects.first()
        password_reset_code = user.change_configuration.get("password_reset_code")
        assert password_reset_code is not None
        
        # Try wrong username
        rv = self.app.get("/password_reset/not_there/" + password_reset_code + "/")
        assert rv.status_code == 404
        
        # Try wrong password reset code
        rv = self.app.get("/password_reset/" + self.user_dict().get("username") + "/bad_code/")
        assert rv.status_code == 404
        
        # Do right password reset code
        rv = self.app.post("/password_reset/"+ self.user_dict().get("username") + "/" + password_reset_code + "/",
                           data=dict(password="newpassword",
                           confirm="newpassword"),
                           follow_redirects=True)
        assert "Your password has been updated" in str(rv.data)
        user = User.objects.first()
        assert user.change_configuration == {}
        
        # Try logging in with new password
        rv = self.app.post("/login/", data=dict(
             username=self.user_dict()["username"],
             password="newpassword")
             )
        # Check the session is set
        with self.app as c:
            rv = c.get("/")
            assert session.get("username") == self.user_dict()["username"]

    def test_change_password(self):
        # Create a user
        self.app.post("/register/", data=self.user_dict())
        
        # Confirm the user
        user = User.objects.get(username=self.user_dict()["username"])
        code = user.change_configuration.get("confirmation_code")
        rv = self.app.get("/confirm/" + user.username + "/" + code + "/")
        
        # Login the user
        rv = self.app.post("/login/", data=dict(
            username=self.user_dict()["username"],
            password=self.user_dict()["password"]
            ))
        
        # Change the password
        rv = self.app.post("/change_password/", data=dict(
            current_password=self.user_dict()["password"],
            password="newpassword",
            confirm="newpassword"), follow_redirects=True)
        assert "Your password has been updated" in str(rv.data)
        
        # Try logging in with new password
        rv = self.app.post("/login/", data=dict(
             username=self.user_dict()["username"],
             password="newpassword")
             )
        # Check the session is set
        with self.app as c:
            rv = c.get("/")
            assert session.get("username") == self.user_dict()["username"]
