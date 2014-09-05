from helper.urls import patterns,include,url




urlpatterns = patterns('',
    ('accounts',include('accounts.urls')),
    ('',include('dashboard.urls')),
    #('/sales/',include('sales.urls')),
    #('/catalog/',include('catalog.urls')),
    #('/customer/',include('customers.urls')),
)