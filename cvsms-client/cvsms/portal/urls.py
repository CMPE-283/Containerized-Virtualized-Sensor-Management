from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [

    url(r'^$', views.UserLoginView.as_view(), name='login'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add$', views.AddSensor.as_view(), name='add_sensor'),
    url(r'^logout$', views.logoutView, name='logout'),
    url(r'^dashboard/delete/(?P<pk>[0-9]+)/$', views.delete_sensor, name="delete"),
    url(r'^sample_app$', views.SampleApp.as_view(), name='sample_app'),
    url(r'^sample_app/(?P<pk>[0-9]+)/$', views.api, name='api'),
]