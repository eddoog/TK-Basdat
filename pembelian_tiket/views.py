from django.shortcuts import render

# Create your views here.
def pembelian_tiket(request):
    return render(request, 'pembelian_tiket.html')
# Create your views here.
def beli_tiket(request):
    return render(request, 'beli_tiket.html')
