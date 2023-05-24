from django.urls import path
from .views import peminjaman_stadium
from .views import pesan_stadium
from .views import pilih_waktu_stadium

app_name = 'peminjaman_stadium'

urlpatterns = [
    path('', peminjaman_stadium, name='peminjaman_stadium'),
    path('pesan', pesan_stadium, name='pesan_stadium'),
    path('pesan/pilih_waktu', pilih_waktu_stadium, name='pilih_waktu_stadium'),
]