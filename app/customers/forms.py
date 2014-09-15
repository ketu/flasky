from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from flask.ext.babel import gettext as _

from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,Length,Regexp,EqualTo
from wtforms import ValidationError


from .model import Customer,Group
from app.dashboard.model import Website


def get_enabled_group():
    return Group.query.all()

def get_enabled_website():
    return Website.query.all()

class CustomerForm(Form):
    website_id = QuerySelectField(_('Website'),query_factory=get_enabled_website)
    group_id = QuerySelectField(_('Group'),query_factory=get_enabled_group,allow_blank=True)
    email = StringField(_('Email'),validators=[DataRequired(),Email()])
    firstname = StringField(_('First name'),validators=[DataRequired()])
    lastname = StringField(_('Last name'),validators=[DataRequired()])
    submit = SubmitField(_('Submit'))



    def validate_email(self, field):
        if Customer.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))