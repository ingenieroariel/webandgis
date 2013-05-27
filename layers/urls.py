from django.conf.urls import patterns, url
from layers.views import index, calculate, detail

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'calculate/$', calculate, name='calculate'),
    url(r'^(?P<layer_slug>[\w\-]+)/$', detail, name='detail'),
)
