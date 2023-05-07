from django.shortcuts import render
# Create your views here.

def pertandingan_belum_lengkap(request):
    return render(request, 'pertandingan_belum_lengkap.html')

def pertandingan_group_stage_pertama(request):
    return render(request,'group_stage_pertama.html')

def peristiwa_tim(request):
    return render(request,'peristiwa_tim.html')

def pertandingan_group_stage_kedua(request):
    return render(request,'group_stage_kedua.html')

def playoff(request):
    return render(request,'playoff_stage.html')

def akhir_musim(request):
    return render(request,'akhir_musim.html')