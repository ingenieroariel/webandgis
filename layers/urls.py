from django.conf.urls import patterns, url
from layers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<layer_slug>[\w\-]+)/$', views.detail, name='detail'),
)
