from flask import Flask
from flask.ext.mongoengine import MongoEngine


db = MongoEngine()


def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    
    app.config.update(config_overrides)
    # Get environment from settings.py, but allow any instance that wants to
    # override with updated settings to do so
    
    db.init_app(app)  # Initialize the database
    
    from user.views import user_app
    app.register_blueprint(user_app)
    
    from relationship.views import relationship_app
    app.register_blueprint(relationship_app)
    
    from feed.views import feed_app
    app.register_blueprint(feed_app)
    
    return app
