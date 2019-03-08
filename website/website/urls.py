from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from website import views

urlpatterns = [
    url(r'^$', views.Dashboard.as_view(), name="dashboard"),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^admin/', admin.site.urls)
]
