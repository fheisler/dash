from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from homepage import views

urlpatterns = patterns('',
    url(r'^$', include('homepage.urls')),
    url(r'^index/', include('homepage.urls')),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^signout/', views.sign_out, name='signout'),
    url(r'^user/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
