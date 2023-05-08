from django.urls import path
from pembelian_tiket.views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pilih_stadium, name='pilih_stadium'),
    path('list_waktu_stadium',list_waktu_stadium, name='list_waktu_stadium'),
    path('beli_tiket', beli_tiket, name='beli_tiket'),
    path('list_pertandingan', list_pertandingan, name='list_pertandingan'),
]
