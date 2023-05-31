from django.urls import path
from mulai_pertandingan.views import mulai_pertandingan, pilih_peristiwa

app_name = 'mulai_pertandingan'

urlpatterns = [
    path('', mulai_pertandingan, name='mulai_pertandingan'),
    path('pilih_peristiwa/<str:nama_tim>/<uuid:id_pertandingan>/', pilih_peristiwa, name='pilih_peristiwa'),
    # path('/rapat', rapat, name='rapat')
]
