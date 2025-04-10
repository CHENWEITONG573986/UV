import wtforms
from pyexpat.errors import messages
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db

class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(max=4,min=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])

    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="验证码不存在，请重新获取")
        if captcha != captcha_model.captcha:
            raise wtforms.ValidationError(message="验证码错误")
        else:
            db.session.delete(captcha_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])

class PermissionsForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=1,max=20,message="用户名格式错误")])
    permissions = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])