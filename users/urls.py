from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns(
    '',
    url(r'signin/$', 'django.contrib.auth.views.login',
        {'template_name': 'users/signin.html'}, name='signin'),
    url(r'signout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='signout'),
)
