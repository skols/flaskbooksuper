from mongoengine import CASCADE


from application import db
from utilities.common import utc_now_ts as now
from user.models import User


class Relationship(db.Document):
    # Set up some constants
    FRIENDS = 1
    BLOCKED = -1
    
    # Set up choices; tuple of tuples
    # Choices limit the number of options a field can have.
    # Choices allows to provide a list to be associated with the field's values.
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
    
    def is_friend(self, user):
        if user:
            return self.get_relationship(user, self.to_user)
        else:
            return None
    
    # A static method doesn't need an instance of the class to be used.
    # A static method allows to use it globally on the class.
    # Get relationship from two users
    @staticmethod
    def get_relationship(from_user, to_user):
        if from_user == to_user:
            return "SAME"
        rel = Relationship.objects.filter(
            from_user=from_user,
            to_user=to_user
            ).first()
        if rel and rel.rel_type == Relationship.FRIENDS:
            if rel.status == Relationship.PENDING:
                return "FRIENDS_PENDING"
            if rel.status == Relationship.APPROVED:
                return "FRIENDS_APPROVED"
        elif rel and rel.rel_type == Relationship.BLOCKED:
            return "BLOCKED"
        else:
            reverse_rel = Relationship.objects.filter(
                from_user=to_user,
                to_user=from_user
                ).first()
            if reverse_rel and reverse_rel.rel_type == Relationship.FRIENDS:
                if reverse_rel.status == Relationship.PENDING:
                    return "REVERSE_FRIENDS_PENDING"
            elif reverse_rel and reverse_rel.rel_type == Relationship.BLOCKED:
                return "REVERSE_BLOCKED"
            return None
    
    # Indexes; compound indexes which are in ()
    meta = {
        "indexes": [("from_user", "to_user"), ("from_user", "to_user", "rel_type", "status")]
    }
