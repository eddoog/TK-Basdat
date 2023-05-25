from django.shortcuts import redirect, render
from utils.users import check_username, check_role, get_pelatih, get_pemain
from utils.query import query
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def tim(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    context = {'list_pemain': get_pemain(namaTim),
               'list_pelatih': get_pelatih(namaTim)}

    return render(request, 'daftarpemainpelatih.html', context)


@csrf_exempt
def changeCaptain(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    captain_id = request.POST.get('id_kapten')

    updatePemainStatus = query(
        f''' UPDATE PEMAIN SET is_captain = true WHERE id_pemain = '{captain_id}' ''')

    if (isinstance(updatePemainStatus, Exception)):
        return redirect('/manajer/tim/', {
            'error': updatePemainStatus.args[0].split("\n")[0]
        })

    return redirect('/manajer/tim/')


@csrf_exempt
def removePlayer(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    player_id = request.POST.get('id_pemain')

    query(
        f''' UPDATE PEMAIN SET nama_tim = NULL WHERE id_pemain = '{player_id}' ''')

    return redirect('/manajer/tim/')


@csrf_exempt
def removeCoach(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    coach_id = request.POST.get('id_pelatih')

    query(
        f'''UPDATE PELATIH SET nama_tim = NULL WHERE id_pelatih = '{coach_id}' ''')

    return redirect('/manajer/tim/')


@csrf_exempt
def daftar_tim(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    if (request.session.get('namaTim') is not None):
        return redirect('/manajer/tim')

    if (request.method == "POST"):
        response = HttpResponse()
        namaTim = request.POST.get('namaTim')
        namaUniversitas = request.POST.get('namaUniversitas')

        insertTimStatus = query(
            f''' INSERT INTO TIM (nama_tim, universitas) VALUES ('{namaTim}', '{namaUniversitas}') ''')
        if (isinstance(insertTimStatus, Exception)):
            return JsonResponse({'error': "Nama tim sudah pernah dipakai"}, status=400)

        idManajer = query(f'''
            SELECT id_manajer FROM MANAJER WHERE username = '{username}'
            ''')[0]['id_manajer']
        query(f'''
            INSERT INTO TIM_MANAJER (id_manajer, nama_tim)
            VALUES ('{idManajer}', '{namaTim}')
            ''')

        request.session['namaTim'] = namaTim
        response.status_code = 200
        return response

    return render(request, 'daftarTim.html')


@csrf_exempt
def daftar_pelatih(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    context = {
        'list_pelatih': query(f''' 
        SELECT *
        FROM NON_PEMAIN NP
        JOIN PELATIH P ON NP.id = P.id_pelatih
        JOIN SPESIALISASI_PELATIH SP ON P.id_pelatih = SP.id_pelatih
        WHERE P.nama_tim IS NULL
        ''')
    }

    if (request.method == "POST"):
        response = HttpResponse()
        idPelatih = request.POST.get('coachId')

        updatePelatihStatus = query(
            f''' 
            UPDATE PELATIH 
            SET nama_tim = '{namaTim}' 
            WHERE id_pelatih = '{idPelatih}' 
            ''')
        if (isinstance(updatePelatihStatus, Exception)):
            return JsonResponse({'error': updatePelatihStatus.args[0].split("\n")[0]}, status=400)

        response.status_code = 200
        return response

    return render(request, 'formulirDaftarPelatih.html', context)


@csrf_exempt
def daftar_pemain(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    namaTim = request.session.get('namaTim')

    if (namaTim is None):
        return redirect('/manajer/daftar-tim')

    context = {
        'list_pemain': query(f''' 
        SELECT * 
        FROM PEMAIN 
        WHERE nama_tim IS NULL 
        ''')
    }

    if (request.method == "POST"):
        response = HttpResponse()
        idPemain = request.POST.get('playerId')

        updatePemainStatus = query(f''' 
        UPDATE PEMAIN 
        SET nama_tim = '{namaTim}' 
        WHERE id_pemain = '{idPemain}' 
        ''')

        if (isinstance(updatePemainStatus, Exception)):
            return JsonResponse({'error': updatePemainStatus.args[0].split("\n")[0]}, status=400)

        response.status_code = 200
        return response

    return render(request, 'formulirDaftarPemain.html', context)
