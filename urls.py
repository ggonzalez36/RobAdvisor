from django.conf.urls import url
from . import views

app_name='roboadvisor'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^(?P<company_id>[0-9]+)/$', views.detail, name='detail'),


    url(r'^(?P<company_id>[0-9]+)/prediction/$', views.createPrediction, name='prediction'),

    url(r'^(?P<company_id>[0-9]+)/graph/$', views.graph, name='graph'),
    url(r'^(?P<company_id>[0-9]+)/predicted/$', views.graphPrediction, name='graphPrediction'),
    url(r'^account/$', views.account, name='account'),

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^(?P<company_id>[0-9]+)/predicted/$', views.graphPrediction, name='graphPrediction'),
    url(r'^asset/(?P<assetId>[0-9]+)/$', views.stockDetails, name='stockDetails')
]