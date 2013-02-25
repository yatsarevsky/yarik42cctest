from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import os

from .vcard import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.contacts, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^request_store/$', views.requests_store, name='requests'),
    url(r'^edit/$', views.edit_page, name='edit_page'),
    url(r'^signup/$', views.accounts_registration, name='sign-up'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': os.path.join(settings.PROJECT_ROOT, 'static/')}
        ),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.PROJECT_ROOT, 'uploads')}
        )
    )
