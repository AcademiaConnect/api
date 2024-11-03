from .views import EventView, EventAutoFillView
from django.urls import path


app_name = 'events'


urlpatterns = [
    path('create/', EventView.as_view(), name='create-event'),
    path('auto_complete/', EventAutoFillView.as_view(), name='auto-complete-event'),
]