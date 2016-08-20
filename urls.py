from django.conf.urls.defaults import *
import scores.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('scores.views',
    (r'^admin/', include(admin.site.urls)),
    (r'^score/', include(scores.urls)),
)

urlpatterns += patterns('',
        (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'scores/login.html'}),

        (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/accounts/login/?next=/score'}),

        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/david/svn/python/django/handicap/media', 'show_indexes': True})
)
