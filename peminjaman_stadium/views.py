from django.shortcuts import render


# Create your views here.
def peminjaman_stadium(request):
    return render(request, 'peminjaman-stadium.html')


def pesan_stadium(request):
    return render(request, 'pesan-stadium.html')


def pilih_waktu_stadium(request):
    return render(request, 'pilih-waktu-stadium.html')
