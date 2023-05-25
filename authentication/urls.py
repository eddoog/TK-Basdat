from django.urls import path
from authentication.views import index, logout

app_name = 'authentication'

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout, name='logout')
]
