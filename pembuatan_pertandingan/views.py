from django.shortcuts import render

def list_pertandingan(request):
    return render(request, 'list_pertandingan.html')

def jadwal_stadium(request):
    return render(request, 'jadwal_stadium.html')

def add_pertandingan(request):
    return render(request, 'add_pertandingan.html')

def buat_pertandingan(request):
    return render(request, 'buat_pertandingan.html')