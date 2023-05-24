from django.urls import path
from dashboard.views import index, logout

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout, name='logout')
]
