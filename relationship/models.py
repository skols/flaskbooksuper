from mongoengine import CASCADE


from application import db
from utilities.common import utc_now_ts as now
from user.models import User


class Relationship(db.Document):
    # Set up some constants
    FRIENDS = 1
    BLOCKED = -1
    
    # Set up choices; tuple of tuples
    RELATIONSHIP_TYPE = (
        (FRIENDS, "Friends"),
        (BLOCKED, "Blocked"),
        )
    
    # Status choices
    PENDING = 0
    APPROVED = 1
    
    STATUS_TYPE = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        )
    
    # Two records per relationship
    # foreign key to a user
    # With CASCADE, all relationships are deleted if user is deleted
    from_user = db.ReferenceField(User, db_field="fu",
                                  reversed_delete_rule=CASCADE)
    to_user = db.ReferenceField(User, db_field="tu",
                                reversed_delete_rule=CASCADE)
    rel_type = db.IntField(db_field="rt", choices=RELATIONSHIP_TYPE)
    status = db.IntField(db_field="s", choices=STATUS_TYPE)
    req_date = db.IntField(db_field="rd", default=now())
    approved_date = db.IntField(db_field="ad", default=0)
    
    # Indexes; compound indexes which are in ()
    meta = {
        "indexes": [("from_user", "to_user"), ("from_user", "to_user", "rel_type", "status")]
    }
