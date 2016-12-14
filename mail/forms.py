from flask_wtf import Form
from wtforms import validators, StringField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed


class MailForm(Form):
    images = FileField(
        "Select images",
        render_kw={"multiple": True},
        validators=[
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Only JPEG, PNG, and \
                        GIFs allowed")
                        ]
        )
    mail_message=StringField("Mail",
        widget=TextArea(),
        validators=[
            validators.DataRequired(),
            validators.Length(max=1024)]
    )
