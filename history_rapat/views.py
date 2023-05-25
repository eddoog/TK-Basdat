from django.shortcuts import render, redirect
from django.db import connection
from utils.users import check_username, check_role

# Create your views here.


def history_rapat(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role == 'Penonton'):
        return redirect('/dashboard')

    if request.method == 'GET':
        print('Menampilkan history rapat')
        # print(request.session['akun_pengguna'])

        with connection.cursor() as cursor:
            cursor.execute("""
                                SELECT r.id_pertandingan, string_agg(nama_tim, ' vs ') as rapat_tim, np.nama_depan, s.nama, datetime
                                FROM D02.rapat r, D02.pertandingan p, D02.tim_pertandingan tp, D02.stadium s, D02.non_pemain np
                                WHERE r.id_pertandingan = p.id_pertandingan and p.id_pertandingan = tp.id_pertandingan and p.stadium = s.id_stadium and r.perwakilan_panitia = np.id
                                GROUP BY r.id_pertandingan, np.nama_depan, stadium, s.nama, datetime;
                                """)
            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            print(data)

        context = {'data': data}

        return render(request, 'history-rapat.html', context)
