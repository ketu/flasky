#/usr/bin/env python
#-*- coding:utf8 -*-

from importlib import import_module
from app.settings import INSTALLED_APPLICATION
from app.core import manager,app

if __name__ == '__main__':
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


    manager.run()
    #app.run(debug=True)