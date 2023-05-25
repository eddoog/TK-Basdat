from django.urls import path
<<<<<<< HEAD
from mulai_pertandingan.views import *
=======
from mulai_pertandingan.views import mulai_pertandingan, pilih_peristiwa
>>>>>>> 01ac25c1ccd1cc8b99b837a5a1d995121080f1c4

app_name = 'mulai_pertandingan'

urlpatterns = [
    path('', mulai_pertandingan, name='mulai_pertandingan'),
<<<<<<< HEAD
    path('pilih_peristiwa', pilih_peristiwa, name='pilih_peristiwa'),
    
=======
    path('pilih_peristiwa/<str:nama_tim>/<uuid:id_pertandingan>/', pilih_peristiwa, name='pilih_peristiwa'),
>>>>>>> 01ac25c1ccd1cc8b99b837a5a1d995121080f1c4
    # path('/rapat', rapat, name='rapat')
]
