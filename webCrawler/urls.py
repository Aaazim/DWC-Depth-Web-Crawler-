from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.startApp, name='startApp'),
        url(r'^likepost/$', views.likePost, name='likepost'),
   ]