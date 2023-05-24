from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from utils.query import query
from utils.users import get_role
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import uuid


@csrf_exempt
def index(request):
    if (request.method == 'GET'):
        return render(request, 'index.html', {})

    # POST request
    if (request.POST.get('type') == 'login'):
        response = HttpResponse()
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the username and password match
        query_str = f''' SELECT * FROM User_System WHERE Username = '{username}' AND Password = '{password}' '''
        user_list = query(query_str)

        print(user_list)
        if len(user_list) != 0:  # User found
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            response.set_cookie('role', get_role(username))
            response.status_code = 200
            return response
        else:  # User not found
            response.delete_cookie('username')
            response.delete_cookie('password')
            response.delete_cookie('role')
            response.status_code = 404
            return response

    elif (request.POST.get('type') == 'register'):
        response = HttpResponse()
        id = uuid.uuid4()
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        namaDepan = request.POST.get('namaDepan')
        namaBelakang = request.POST.get('namaBelakang')
        alamat = request.POST.get('alamat')
        nomorHP = request.POST.get('nomorHP')
        listStatus = request.POST.getlist('status[]')

        query_str_usersystem = f''' INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}') '''

        query_str_nonpemain = f''' INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, nomor_hp, email, alamat) VALUES ('{id}', '{namaDepan}', '{namaBelakang}', '{nomorHP}','{email}', '{alamat}')'''

        insertUserSystemStatus = query(query_str_usersystem)
        if isinstance(insertUserSystemStatus, Exception):
            return JsonResponse({'error': insertUserSystemStatus.args[0].split("\n")[0]}, status=400)
        else:
            query(query_str_nonpemain)

            for status in listStatus:
                query(
                    f''' INSERT INTO STATUS_NON_PEMAIN VALUES ('{id}', '{status}')''')

            if (role == 'panitia'):
                jabatan = request.POST.get('jabatan')
                query(
                    f''' INSERT INTO PANITIA VALUES ('{id}' , '{jabatan}', '{username}')''')
            elif (role == 'manajer'):
                query(
                    f''' INSERT INTO MANAJER VALUES ('{id}' , '{username}')''')
            elif (role == 'penonton'):
                query(
                    f''' INSERT INTO PENONTON VALUES ('{id}' , '{username}')''')

            response.status_code = 200
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            response.set_cookie('role', role)
            return response

    return HttpResponse("Invalid request")
