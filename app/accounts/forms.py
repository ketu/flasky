from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(Form):
    email = StringField(_('Email'),validators=[DataRequired(),Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember = BooleanField(_('Remember me?'))
    submit = SubmitField(_('Submit'))


