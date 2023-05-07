from manage_pertandingan.views import *
from django.urls import path

app_name = 'manage_pertandingan'

urlpatterns = [
    path('belum_lengkap', pertandingan_belum_lengkap, name='belum_lengkap'),
    path('group_stage_pertama',pertandingan_group_stage_pertama, name='group_stage_pertama'),
    path('group_stage_kedua',pertandingan_group_stage_kedua, name='group_stage_kedua'),
    path('peristiwa_tim', peristiwa_tim, name='peristiwa_tim' ),
    path('playoff', playoff, name='playoff' ),
    path('akhir_musim', akhir_musim, name='akhir_musim' )

]