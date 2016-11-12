from flask import Blueprint, session, render_template


from user.models import User
from feed.models import Feed
from feed.forms import FeedPostForm


home_app = Blueprint("home_app", __name__)

@home_app.route("/")
@home_app.route("/feed/<int:feed_page_num>/", endpoint="feed-home-page")
def home(feed_page_num=1):
    feed_messages_page = False
    
    if session.get("username"):
        form = FeedPostForm()
    
        user = User.objects.filter(
            username=session.get("username")
            ).first()
        
        feed_messages_total = Feed.objects.filter(
            user=user
            ).count()
        
        feed_messages = Feed.objects.filter(
            user=user
            ).order_by("-create_date")
        
        if feed_messages_total > 10:
            feed_messages_page = True
            feed_messages = feed_messages.paginate(page=feed_page_num, per_page=10)
        else:
            feed_messages = feed_messages[:10]
        
        return render_template("home/feed_home.html",
                               user=user,
                               form=form,
                               feed_messages_total=feed_messages_total,
                               feed_messages=feed_messages,
                               feed_messages_page=feed_messages_page,
                               feed_page_num=feed_page_num,
                               )

    else:
        return render_template("home/home.html")
