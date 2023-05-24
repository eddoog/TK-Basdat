from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'dashboard.html')


@csrf_exempt
def logout(request):
    response = HttpResponse()
    response.delete_cookie('username')
    response.delete_cookie('password')
    response.delete_cookie('role')
    response.status_code = 200
    return response
