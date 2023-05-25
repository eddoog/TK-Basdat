from django.shortcuts import render, redirect
from django.db import connection
from utils.users import check_username, check_role


# Create your views here.
def list_pertandingan(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role == 'Panitia'):
        return redirect('/dashboard')

    if request.method == 'GET':
        if (role == "Manajer"):

            username = request.COOKIES.get('username')
            with connection.cursor() as cursor:
                cursor.execute("""
                                        SELECT M.ID_manajer 
                                        FROM D02.manajer M, D02.user_system U 
                                        WHERE U.username = %s AND M.username = U.username;
                                        """, [username])

                columns = [col[0] for col in cursor.description]

                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            id_manajer = data[0]['id_manajer']

            with connection.cursor() as cursor:
                cursor.execute("""
                                        SELECT string_agg(tp.nama_tim, ' vs ') as tim_bertanding, s.nama,
                                        to_char(p.start_datetime, 'DD Month YYYY, HH:MI') || ' - ' || to_char(p.end_datetime, 'HH:MI') as time
                                        FROM D02.pertandingan p
                                        JOIN D02.stadium s ON p.stadium = s.id_stadium
                                        JOIN D02.tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan

                                        JOIN D02.tim_manajer tm on tm.nama_tim = tp.nama_tim
                                        JOIN D02.manajer m on m.id_manajer = tm.id_manajer
                                        WHERE m.id_manajer = %s

                                        GROUP BY s.nama, time;
                                        """, [id_manajer])

                columns = [col[0] for col in cursor.description]

                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                print(data)
        else:
            print("masuk else")
            with connection.cursor() as cursor:
                cursor.execute("""
                                        SELECT string_agg(tp.nama_tim, ' vs ') as tim_bertanding, s.nama,
                                        to_char(p.start_datetime, 'DD Month YYYY, HH:MI') || ' - ' || to_char(p.end_datetime, 'HH:MI') as time
                                        FROM D02.pertandingan p
                                        JOIN D02.stadium s ON p.stadium = s.id_stadium
                                        JOIN D02.tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
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
