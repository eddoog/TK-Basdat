from django.shortcuts import render

# Create your views here.
def pilih_stadium(request):
    return render(request, 'pilih_stadium.html')

def list_waktu_stadium(request):
    return render(request, 'list_waktu_stadium.html')

def list_pertandingan(request):
    return render(request, 'list_pertandingan.html')
# Create your views here.
def beli_tiket(request):
    return render(request, 'beli_tiket.html')
