from django.shortcuts import render

# Create your views here.
def listPertandingan(request):
    return render(request, 'list-pertandingan.html')

def historyRapat(request):
    return render(request, 'history-rapat.html')

def peminjamanStadium(request):
    return render(request, 'peminjaman-stadium.html')

def pesanStadium(request):
    return render(request, 'pesan-stadium.html')

def pilihWaktuStadium(request):
    return render(request, 'pilih-waktu-stadium.html')