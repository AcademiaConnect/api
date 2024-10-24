from .views import EventView
from django.urls import path


app_name = 'events'


urlpatterns = [
    path('create/', EventView.as_view(), name='create-event'),
]