from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
from flask import session


from user.models import User
from relationship.models import Relationship


class FeedTest(unittest.TestCase):
    def create_app(self):
        self.db_name = "flaskbook_test"
        return create_app_base(
            MONGODB_SETTINGS={"DB": self.db_name},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="mySecret!"
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
            confirm="test123",
            )
    
    def user2_dict(self):
        return dict(
            first_name="Nicole",
            last_name="Di Bella",
            username="nicole",
            email="nicole@example.com",
            password="test123",
            confirm="test123",
            )
    
    def user3_dict(self):
        return dict(
            first_name="Cullen",
            last_name="Bohannon",
            username="cullen",
            email="cullen@example.com",
            password="test123",
            confirm="test123",
            )
    
    def test_feed_posts(self):
        # Register user1
        rv = self.app.post("/register/", data=self.user1_dict(),
                           follow_redirects=True)
        
        # Login user1
        rv = self.app.post("/login/", data=dict(
            username=self.user1_dict()["username"],
            password=self.user1_dict()["password"],
            ))
        
        # Post a message
        rv = self.app.post("/message/add/", data=dict(
            post="Test Post #1 User 1",
            to_user=self.user1_dict()["username"],
            ), follow_redirects=True)
        assert "Test Post #1 User 1" in str(rv.data)
        
        # Register user2
        rv = self.app.post("/register/", data=self.user2_dict(),
                           follow_redirects=True)
        
        # Make friends with user2
        rv = self.app.get("/add_friend/" + self.user2_dict()["username"] + "/",
                          follow_redirects=True)
        
        # Login user2 and confirm friend user1
        rv = self.app.post("/login/", data=dict(
            username=self.user2_dict()["username"],
            password=self.user2_dict()["password"],
            ))
        rv = self.app.get("/add_friend/" + self.user1_dict()["username"] + "/",
                          follow_redirects=True)
        
        # Login user1 again
        rv = self.app.post("/login/", data=dict(
            username=self.user1_dict()["username"],
            password=self.user1_dict()["password"],
            ))
        
        # Post a message
        rv = self.app.post("/message/add/", data=dict(
            post="Test Post #2 User 1",
            to_user=self.user1_dict()["username"],
            ), follow_redirects=True)
        
        # Post a message to user2
        rv = self.app.post("/message/add/", data=dict(
            post="Test Post User 1 to User 2",
            to_user=self.user2_dict()["username"],
            ), follow_redirects=True)
        
        # Login user2 again
        rv = self.app.post("/login/", data=dict(
            username=self.user2_dict()["username"],
            password=self.user2_dict()["password"],
            ))
        rv = self.app.get("/")
        assert "Test Post #2 User 1" in str(rv.data)
        assert "Test Post User 1 to User 2" in str(rv.data)
        
        # Register user3
        rv = self.app.post("/register/", data=self.user3_dict(),
                           follow_redirects=True)
        
        # User3 make friends with user2
        rv = self.app.get("/add_friend/" + self.user2_dict()["username"] + "/",
                          follow_redirects=True)
        
        # Login user1
        rv = self.app.post("/login/", data=dict(
            username=self.user1_dict()["username"],
            password=self.user1_dict()["password"],
            ))
        
        # User1 block user3
        rv = self.app.get("/block/" + self.user3_dict()["username"] + "/",
                          follow_redirects=True)
        
        # Login user2
        rv = self.app.post("/login/", data=dict(
            username=self.user2_dict()["username"],
            password=self.user2_dict()["password"],
            ))
        
        # User2 confirm friends with user3
        rv = self.app.get("/add_friend/" + self.user3_dict()["username"] + "/",
                          follow_redirects=True)
        
        # User2 post a message to user3
        rv = self.app.post("/message/add/", data=dict(
            post="Test Post User 2 to User 3",
            to_user=self.user3_dict()["username"],
            ), follow_redirects=True)
        
        # Login user1
        rv = self.app.post("/login/", data=dict(
            username=self.user1_dict()["username"],
            password=self.user1_dict()["password"],
            ))
        
        # Check user1 doesn't see user2's post to user3 (user1 blocked user3)
        rv = self.app.get("/")
        assert "Test Post User 2 to User 3" not in str(rv.data)
        