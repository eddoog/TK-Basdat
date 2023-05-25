from django.urls import path
from .views import peminjaman_stadium
from .views import pesan_stadium
from .views import edit

app_name = 'peminjaman_stadium'

urlpatterns = [
    path('', peminjaman_stadium, name='peminjaman_stadium'),
    path('pesan', pesan_stadium, name='pesan_stadium'),
    path('edit', edit, name='edit'),
]