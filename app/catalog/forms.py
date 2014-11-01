from flask.ext.wtf import Form
from flask.ext.mongoengine.wtf import model_form

from flask.ext.babel import gettext as _

from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,Length,Regexp,EqualTo
from wtforms import ValidationError

from .model import Category,ProductGallery,Product
from app.dashboard.model import Website

def get_category_tree():

    """
    SELECT CONCAT( REPEAT(' ', COUNT(parent.name) - 1), node.name) AS name
    FROM nested_category AS node,
            nested_category AS parent
    WHERE node.lft BETWEEN parent.lft AND parent.rgt
    GROUP BY node.name
    ORDER BY node.lft;
    """

    result = [(None,"-- Please Select --")]
    categories = Category.objects().order_by("lft")
    for category in categories:
        result.append((str(category.id),category.name))
    return result

class CategoryForm(Form):
    parent = SelectField(_("Parent"),choices=get_category_tree())
    name = StringField(_('Name'),validators=[DataRequired()])
    submit = SubmitField(_('Submit'))


    def validate_parent(form,field):
        if field.data:
            category = Category.objects.get(pk=field.data)
            if category:
                field.data = category
            else:
                raise ValidationError('Parent must exists')

        else:
            field.data = None



