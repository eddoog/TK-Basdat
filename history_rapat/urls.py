from django.urls import path
from .views import history_rapat

app_name = 'history_rapat'

urlpatterns = [
    path('', history_rapat, name='history_rapat'),
]