from django.urls import path
from pembelian_tiket.views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pilih_stadium, name='pilih_stadium'),
    path('beli_tiket',beli_tiket, name='beli_tiket'),
    path('pilih_pertandingan', pilih_pertandingan, name='pilih_pertandingan'),
    path('pesan_tiket', pesan_tiket, name='pesan_tiket'),
]
