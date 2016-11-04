from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
from flask import session


from user.models import User
from relationship.models import Relationship


class RelationshipTest(unittest.TestCase):
    def create_app(self):
        self.db_name = "flaskbook_test"
        return create_app_base(
            MONGODB_SETTINGS={"DB": self.db_name},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="mySecret!",
            )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def user1_dict(self):
        return dict(
            first_name="Michael",
            last_name="Skolnik",
            username="michael",
            email="michael@example.com",
            password="test123",
            confirm="test123"
            )

    def user2_dict(self):
        return dict(
            first_name="Nicole",
            last_name="Di Bella",
            username="nicole",
            email="nicole@example.com",
            password="test123",
            confirm="test123"
            )

    def test_friends_operations(self):
        rv = self.app.post("/register/", data=self.user1_dict(),
                           follow_redirects=True)
        assert User.objects.filter(username=self.user1_dict()["username"]).count() == 1
        rv = self.app.post("/register/", data=self.user2_dict(),
                           follow_redirects=True)
        assert User.objects.filter(username=self.user2_dict()["username"]).count() == 1
        
        rv = self.app.post("/login/", data=dict(
            username=self.user1_dict()["username"],
            password=self.user1_dict()["password"]
        ))
        
        rv = self.app.get("/add_friend/" + self.user2_dict()["username"] + "/",
                          follow_redirects=True)
        assert "relationship-friends-requested" in str(rv.data)
        
        relcount = Relationship.objects.count()
        assert relcount == 1
        
        rv = self.app.post("/login/", data=dict(
            username=self.user2_dict()["username"],
            password=self.user2_dict()["password"]
        ))
        
        rv = self.app.get("/" + self.user1_dict()["username"] + "/")
        assert "relationship-reverse-friends-requested" in str(rv.data)
        