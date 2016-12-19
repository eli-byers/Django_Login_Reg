from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='root'),
    url(r'^home$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
]
