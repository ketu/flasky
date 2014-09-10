#/usr/bin/env python
#-*- coding:utf8 -*-

import os,importlib

from app.core import manager,app

from app import settings
#from app.accounts.views import account
#from app.dashboard.views import system
#from app.sales.views import sales
#from app.customers.views import customers
#from app.catalog.views import catalog


if __name__ == '__main__':
    for _app in settings.INSTALLED_APPLICATION:
        args = ['app',_app,'views']
        try :
            _module = importlib.import_module(".".join(args))
        except ImportError as e:
            pass

        #print(_module)




    #app.register_blueprint(account)
    #app.register_blueprint(system)
    manager.run()
    #app.run(debug=True)


