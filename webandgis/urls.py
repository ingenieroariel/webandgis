from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r'^layers/', include('layers.urls', namespace='layers')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
