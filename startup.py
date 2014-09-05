#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from importlib import import_module
from flask import Blueprint
from app.settings import INSTALLED_APPLICATION,TEMPLATE_FOLDER
from app.core import manager,app
from app.core.urls import urlpatterns

if __name__ == '__main__':


    for blueprint,urls in urlpatterns.iteritems():
        blueprint,prefix = blueprint.split(":")
        _blueprint = None
        if blueprint:
            _blueprint = Blueprint(blueprint, __name__,url_prefix=prefix,template_folder=os.path.join(TEMPLATE_FOLDER,blueprint))


        for index,view in urls.iteritems():
            if _blueprint:
                _blueprint.add_url_rule(view[0],view_func=view[1])
            else:
                app.add_url_rule(view[0],view_func=view[1])


        if _blueprint:
            app.register_blueprint(_blueprint)

        #print(blueprint)

        #if blueprint:
            #simple_page = Blueprint('blueprint', __name__,url_prefix=blueprint)


    manager.run()
    #app.run(debug=True)



"""
    for _app in INSTALLED_APPLICATION:
        try :
            _ap = import_module('app.'+_app+'.urls')
            if _ap.urlpatterns :
                for _url in _ap.urlpatterns:
                    if len(_url) < 2:
                        continue
                    app.add_url_rule(_url[0],view_func=_url[1])
        except Exception as e:
            print(e)
            continue
"""