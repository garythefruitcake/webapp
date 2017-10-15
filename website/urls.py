from django.conf.urls import include, url
from django.contrib import admin
from studentsprofile import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^studentsprofile', include('studentsprofile.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^(?P<profile_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_profile/$', views.create_profile, name='create_profile'),
    url(r'^(?P<profile_id>[0-9]+)/delete_profile/$', views.delete_profile, name='delete_profile'),
    url(r'^(?P<profile_id>[0-9]+)/create_detail/$', views.create_profile, name='create_detail'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^log_detail/(?P<filter_by>[a-zA_Z]+)/$', views.log_detail, name='log_detail'),
]
