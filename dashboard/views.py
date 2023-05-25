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
    context = {}
    non_pemain = query(f''' 
        SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, string_agg(status, ', ') as status, jabatan
        FROM NON_PEMAIN np join status_non_pemain snp 
        on np.id = snp.id_non_pemain 
        join panitia p on p.id_panitia = np.id
        WHERE username = '{username}'
        GROUP BY nama_depan, nama_belakang, nomor_hp, email, alamat, jabatan;
        ''')[0]
    list_rapat = query(f'''
    SELECT r.id_pertandingan, t.nama_tim as tim_a, t2.nama_tim as tim_b,  r.datetime, np1.nama_depan AS p_fname,
            np1.nama_belakang AS p_lname,
            np2.nama_depan AS ma_fname, np2.nama_belakang AS ma_lname,
            np3.nama_depan AS mb_fname, np3.nama_belakang AS mb_lname, r.isi_rapat
            FROM rapat r
            INNER JOIN non_pemain np1 ON np1.id = r.perwakilan_panitia
            INNER JOIN non_pemain np2 ON np2.id = r.manajer_tim_a
            INNER JOIN non_pemain np3 ON np3.id = r.manajer_tim_b
            INNER JOIN tim_manajer t on np2.id = t.id_manajer
            INNER JOIN tim_manajer t2 on np3.id = t2.id_manajer
            WHERE r.datetime > current_timestamp and
            r.perwakilan_panitia = (SELECT id_panitia FROM panitia WHERE username = '{username}')
        ''')

    context['nama_depan'] = non_pemain["nama_depan"]
    context['nama_belakang'] = non_pemain["nama_belakang"]
    context['no_hp'] = non_pemain["nomor_hp"]
    context['email'] = non_pemain["email"]
    context['alamat'] = non_pemain["alamat"]
    context['status'] = non_pemain["status"].upper()
    context['jabatan'] = non_pemain["jabatan"].upper()
    context['list_rapat'] = list_rapat
    return context


def getContextPenonton(request, username):
    context = {}
    id = query(f''' SELECT id_penonton FROM PENONTON WHERE username = '{username}' ''')[
        0]['id_penonton']
    non_pemain = query(f''' 
        SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, string_agg(status, ', ') as status
        FROM NON_PEMAIN np join status_non_pemain snp 
        on np.id = snp.id_non_pemain 
        WHERE id = '{id}'
        GROUP BY nama_depan, nama_belakang, nomor_hp, email, alamat;
        ''')[0]
    pemesanan_tiket = query(f''' 
        SELECT p.ID_Pertandingan, p.Start_Datetime, p.End_Datetime, s.Nama as nama_stadium, string_agg(tb.nama_tim, ' vs. ') as nama_tim, pt.jenis_tiket
        FROM Pembelian_Tiket AS pt INNER JOIN Pertandingan AS p ON 
        pt.id_pertandingan = p.ID_Pertandingan INNER JOIN Stadium AS s ON 
        p.Stadium = s.ID_Stadium 
        join tim_pertandingan tb on tb.id_pertandingan = p.id_pertandingan
        WHERE pt.id_penonton = '{id}' AND
        p.Start_Datetime > NOW()
        GROUP BY p.ID_Pertandingan, p.Start_Datetime, p.End_Datetime, nama_stadium, pt.jenis_tiket
    ''')[0]

    context['nama_depan'] = non_pemain["nama_depan"]
    context['nama_belakang'] = non_pemain["nama_belakang"]
    context['no_hp'] = non_pemain["nomor_hp"]
    context['email'] = non_pemain["email"]
    context['alamat'] = non_pemain["alamat"]
    context['status'] = non_pemain["status"].upper()
    context['start_datetime'] = pemesanan_tiket["start_datetime"]
    context['end_datetime'] = pemesanan_tiket["end_datetime"]
    context['nama_stadium'] = pemesanan_tiket["nama_stadium"]
    context['nama_tim'] = pemesanan_tiket["nama_tim"]
    context['jenis_tiket'] = pemesanan_tiket["jenis_tiket"]

    return context
