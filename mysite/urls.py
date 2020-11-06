"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.conf.urls import url
from . import view, testdb
from django.views.generic import TemplateView
from django.contrib import admin

import myapp.urls

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^api/', include(myapp.urls)),

    #url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^test_1$', testdb.testdb1),
    url(r'^api/add2$', testdb.add_strategy),
    url(r'^api/getBut$', testdb.get_strategy_name),#
    url(r'^api/add4$', testdb.get_strategy),
    url(r'^api/add5$', testdb.update_state),
    url(r'^api/return_Code$', testdb.return_Code),
    url(r'^api/get_result$', testdb.get_result),
    url(r'', TemplateView.as_view(template_name="index.html")),

]