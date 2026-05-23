from django.urls import path

from . import views


urlpatterns = [
    path('', views.register_event, name='event_register'),
]
