from pembuatan_pertandingan.views import *
from django.urls import path

app_name = 'pembuatan_pertandingan'

urlpatterns = [
    path('list_pertandingan', list_pertandingan, name='list_pertandingan' ),
    path('add_pertandingan',add_pertandingan, name='add_pertandingan'),
    path('jadwal_stadium',jadwal_stadium, name='jadwal_stadium'),
    path('buat_pertandingan',buat_pertandingan, name='buat_pertandingan'),
]