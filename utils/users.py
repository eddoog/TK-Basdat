from django.shortcuts import redirect
from utils.query import query


def get_role(username):
    find_user = f''' SELECT * FROM MANAJER WHERE username = '{username}' '''
    response = query(find_user)
    if (len(response) != 0):
        return 'Manajer'

    find_user = f''' SELECT * FROM PENONTON WHERE username = '{username}' '''
    response = query(find_user)
    if (len(response) != 0):
        return 'Penonton'

    return 'Panitia'


def check_username(request):
    username = request.COOKIES.get('username', None)

    return username


def check_role(request):
    role = request.COOKIES.get('role', None)

    return role


def get_pemain(nama_tim):
    response = query(f'''
        SELECT * FROM PEMAIN 
        WHERE nama_tim = '{nama_tim}' 
        ORDER BY is_captain DESC
        ''')
    return response


def get_pelatih(nama_tim):
    response = query(f'''
        SELECT id, nama_depan, nama_belakang, nomor_hp,email, alamat, string_agg(spesialisasi, ', ') as spesialisasi
        FROM NON_PEMAIN NP 
        JOIN SPESIALISASI_PELATIH SP on NP.id = SP.id_pelatih
        WHERE NP.id in (
        SELECT id_pelatih from pelatih
        where nama_tim = '{nama_tim}'
        )
        GROUP BY id, nama_depan, nama_belakang, nomor_hp,email, alamat
        ''')
    return response
