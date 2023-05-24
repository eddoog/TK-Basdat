from django.shortcuts import render
from django.db import connection

# Create your views here.
def list_pertandingan(request):
     if request.method == 'GET':
            print('Menampilkan list pertandingan')
            # print(request.session['akun_pengguna'])

            with connection.cursor() as cursor:
                cursor.execute("""
                                SELECT string_agg(tp.nama_tim, ' vs ') as tim_bertanding, s.nama, to_char(p.start_datetime, 'DD Month YYYY, HH:MM') as time
                                FROM D02.pertandingan p, D02.stadium s, D02.tim_pertandingan tp
                                WHERE p.id_pertandingan = tp.id_pertandingan and p.stadium = s.id_stadium
                                GROUP BY s.nama, time;
                                """)
                columns = [col[0] for col in cursor.description]

                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                print(data)

            context = {'data': data}

            return render(request, 'list-pertandingan.html', context)