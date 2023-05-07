from django.urls import path
from .views import *

app_name = 'manajer'

urlpatterns = [
    path('list-pertandingan', listPertandingan, name='listPertandingan'),
    path('history-rapat', historyRapat, name='historyRapat'),
    path('peminjaman-stadium', peminjamanStadium, name='peminjamanStadium'),
    path('peminjaman-stadium/pesan', pesanStadium, name='pesanStadium'),
    path('peminjaman-stadium/pesan/pilih-waktu', pilihWaktuStadium, name='pilihWaktuStadium'),
]