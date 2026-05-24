from django.urls import path

from . import views


urlpatterns = [
    path('', views.register_event, name='event_register'),
    path('api/register/', views.register_event_api, name='event_register_api'),
]
