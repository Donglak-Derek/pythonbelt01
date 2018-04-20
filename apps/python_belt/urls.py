from django.conf.urls import url
from . import views   
urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^user/(?P<id>\d+)$', views.display),
    url(r'^logout$', views.logout),
    url(r'^unfollow/(?P<id>\d+)$', views.unfollow),
]