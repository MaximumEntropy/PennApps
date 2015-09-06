from django.conf.urls import patterns, include, url

from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangoapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index, name='index'),
    url(r'^transcript/trump/$',views.get_trump_example,name='trump'),
    url(r'^transcript/buffet/$',views.get_buffet_example,name='buffet'),
    url(r'^transcript/(?P<file_name>\w+)/$',views.process_new_file,name='user_upload'),

)
