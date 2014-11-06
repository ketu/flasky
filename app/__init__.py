from flask.ext.babel import gettext as _
from .settings import API_TYPE

def get_api_type_select():
    result = [(None,_("-- Please Select --"))]
    for t in API_TYPE:
        result.append((t,t.capitalize()))

    return result
