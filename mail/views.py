from flask import Blueprint, session, request
from werkzeug import secure_filename
import os


from user.decorators import login_required


mail_app = Blueprint("mail_app", __name__)

@mail_app.route("/mail/new/", methods=["GET", "POST"])
@login_required
def mail_new():
    return "New mail"
