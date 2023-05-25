from django.urls import path
from manajer.views import tim, daftar_tim, daftar_pelatih, daftar_pemain, changeCaptain, removeCoach, removePlayer

app_name = 'manajer'

urlpatterns = [
    path('tim/', tim, name='tim'),
    path('daftar-tim/', daftar_tim, name='daftar_tim'),
    path('tim/change-captain/', changeCaptain, name='changeCaptain'),
    path('tim/daftar-pemain/', daftar_pemain, name='daftar_pemain'),
    path('tim/remove-player/', removePlayer, name='removePlayer'),
    path('tim/daftar-pelatih/', daftar_pelatih, name='daftar_pelatih'),
    path('tim/remove-coach/', removeCoach, name='removeCoach'),
]
