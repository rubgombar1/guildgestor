from django.conf.urls import patterns, include, url
from django.contrib import admin
from giantsapp.views import PlayerView, CustomErrors

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'giants.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/profile', PlayerView.profile),
    url(r'^', include('giantsapp.urls')),
)
handler403=CustomErrors.error403
handler404=CustomErrors.error404