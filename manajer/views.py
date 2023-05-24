from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

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

def historyRapatCode(request):
    history_rapat = query(f"SELECT * FROM RAPAT")
    context = {
        'history_rapat': history_rapat
    }
    return render(request, 'history-rapat.html', context)

def listPertandinganCode(request):
    history_rapat = query(f"SELECT * FROM PERTANDINGAN")
    context = {
        'list_pertandingan': list_pertandingan
    }
    return render(request, 'list-pertandingan.html', context)

