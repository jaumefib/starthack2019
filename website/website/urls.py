from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from website import views

urlpatterns = [
    url(r'^$', views.Dashboard.as_view(), name="dashboard"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^admin/', admin.site.urls)
]
