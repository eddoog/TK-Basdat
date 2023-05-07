from django.urls import path
from pembelian_tiket.views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pembelian_tiket, name='pembelian_tiket'),
    path('/beli_tiket', beli_tiket, name='beli_tiket')
]
