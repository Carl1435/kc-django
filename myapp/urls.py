
from django.conf.urls import url, include

from . import views
urlpatterns = [
    url(r'js_hsb$', views.js_hsb),
    url(r'add_zd$', views.add_zd),
    url(r'add_zxzs$', views.add_zxzs),
    url(r'add_stockdetail$', views.add_stockdetail),
    url(r'add_stockdayK$', views.add_stockdayK),
    url(r'enter$', views.enter),
    url(r'add_datamain$', views.add_datamain),
    url(r'js_hsb_code$', views.js_hsb_code),
    url(r'add_business$', views.add_business),
    url(r'bk_stockdata$',views.bk_stockdata)
]