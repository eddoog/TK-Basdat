from django.shortcuts import render
from django.db import connection


# Create your views here.
def list_pertandingan(request):
    return render(request, 'list-pertandingan.html')
