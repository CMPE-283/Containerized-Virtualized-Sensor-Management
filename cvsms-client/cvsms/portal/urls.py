from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [

    url(r'^$', views.UserLoginView.as_view(), name='login'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^logout$', views.logoutView, name='logout'),
]