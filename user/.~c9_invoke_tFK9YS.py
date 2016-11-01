from mongoengine import signals
from flask import url_for
import os


from application import db
from utilities.common import utc_now_ts as now
from settings import STATICIMAGE_URL


class User(db.Document):
    username = db.StringField(db_field="u", required=True, unique=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    first_name = db.StringField(db_field="fn", max_length=50)
    last_name = db.StringField(db_field="ln", max_length=50)
    created = db.IntField(db_field="c", default=now())
    bio = db.StringField(db_field="b", max_length=160)
    email_confirmed = db.BooleanField(db_field="ecf", default=False)
    change_configuration = db.DictField(db_field="cc")
    profile_image = db.StringField(db_field="i", default=None)

    # Make username and email all lowercase
    # This method is called before object is written to the database
    @classmethod
    # Do any manipulations you need to do within pre_save
    def pre_save(cls, sender, document, **kwargs):
        document.username = document.username.lower()
        document.email = document.email.lower()
        
    def profile_imgsrc(self, size):
        # return os.path.join(IMAGE_URL, "user", "%s.%s.%s.png" % (self.id,
        #                     self.profile_image, size))
        return os.path.join(IMAGE_URL, "user", "{0}.{1}.{2}.png".format(self.id,
                            self.profile_image, size))

    # Add indexes
    meta = {
        "indexes": ["username", "email", "-created"]
        # -created means sort order reversed to get most recent members
    }


signals.pre_save.connect(User.pre_save, sender=User)
