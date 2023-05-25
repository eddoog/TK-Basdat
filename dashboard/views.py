from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.users import check_username, check_role, get_pemain, get_pelatih
from utils.query import query


def index(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    context = {}
    if (role == 'Manajer'):
        context = getContextManajer(request, username)
    elif (role == 'Panitia'):
        context = getContextPanitia(request, username)
    elif (role == 'Penonton'):
        context = getContextPenonton(request, username)

    context['role'] = role

    return render(request, 'dashboard.html', context)


def getContextManajer(request, username):
    context = {}
    id = query(f''' SELECT id_manajer FROM MANAJER WHERE username = '{username}' ''')[
        0]['id_manajer']
    non_pemain = query(f''' 
        SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, string_agg(status, ', ')  as status
        FROM NON_PEMAIN NP 
        JOIN STATUS_NON_PEMAIN SNP on NP.id = SNP.id_non_pemain 
        WHERE id = '{id}'
        GROUP BY nama_depan, nama_belakang, nomor_hp, email, alamat;
        ''')[0]

    context['nama_depan'] = non_pemain["nama_depan"]
    context['nama_belakang'] = non_pemain["nama_belakang"]
    context['no_hp'] = non_pemain["nomor_hp"]
    context['email'] = non_pemain["email"]
    context['alamat'] = non_pemain["alamat"]
    context['status'] = non_pemain["status"].upper()

    nama_tim = query(
        f''' SELECT nama_tim FROM TIM_MANAJER WHERE id_manajer = '{id}' ''')

    if len(nama_tim) != 0:
        tim = nama_tim[0]['nama_tim']
        universitas = query(f''' SELECT universitas FROM TIM WHERE nama_tim = '{tim}' ''')[
            0]['universitas']
        context['tim'] = tim
        request.session['namaTim'] = tim
        context['universitas'] = universitas
        context['list_pemain'] = get_pemain(tim)
        context['list_pelatih'] = get_pelatih(tim)
    else:
        context['message'] = 'Belum membuat tim'
    return context


def getContextPanitia(request, username):
    return {}


def getContextPenonton(request, username):
    return {}
