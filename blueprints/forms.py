import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
# from extensions import db


# Form：Ued to verify whether the data submitted by the frontend meets the requirements
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Email format error!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="Verification code format error!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="Username format error!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="Wrong password!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="The two passwords do not match!")])

    # Customized validation：
    # 1. Whether the mailbox has been registered
    def validate_email(self, field):    # self: current object      field: Email field in the form
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="This email address has already been registered!")

    # 2. Whether the verification code correct
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_match = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_match:
            raise wtforms.ValidationError(message="Email or verification code error!")
        # else:
        #     # todo：captcha_model can be deleted
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Email format error!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="Wrong password format!")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="Wrong title format!")])
    content = wtforms.StringField(validators=[Length(min=3, message="Wrong content format!")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="Content format error!")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="Question id is required!")])
