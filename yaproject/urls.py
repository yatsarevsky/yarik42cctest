from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import os

from .vcard import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.contacts, name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': os.path.join(settings.PROJECT_ROOT, 'static/')}
        )
    )
