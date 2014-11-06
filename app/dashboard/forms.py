from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,Length,Regexp,EqualTo
from wtforms import ValidationError
from .model import Website
from app import get_api_type_select



class WebsiteForm(Form):

    name = StringField(_('Website name'),validators=[DataRequired()])
    code = StringField(_('Code name'),validators=[DataRequired()])
    type = SelectField(_('Type'),choices=get_api_type_select())
    link = StringField(_('API link'),validators=[DataRequired()])
    key = StringField(_('API key'),validators=[DataRequired()])
    secret = StringField(_('API secret'),validators=[DataRequired()])
    submit = SubmitField(_('Submit'))


    def validate_code(self, field):
        if Website.objects.filter(code=field.data).first():
            raise ValidationError('Code already exists.')
