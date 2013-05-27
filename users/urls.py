from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'login/$', 'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'}, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
