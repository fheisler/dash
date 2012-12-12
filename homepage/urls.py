from django.conf.urls import patterns, url

from homepage import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^signout/', views.sign_out, name='signout'),
)

'''
    url(r'^settings/', views.settings, name='settings'),
    url(r'^signout/', views.sign_out, name='signout'),
'''



#    url(r'^$', TemplateView.as_view(template_name="index.html")),
#    url(r'^settings/', TemplateView.as_view(template_name="settings.html")),
