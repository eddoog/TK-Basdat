from django.shortcuts import render, redirect
import datetime
from utils.query import query


def mulai_rapat(request):
    if request.COOKIES.get('role') != 'Panitia':
        return redirect('/dashboard')

    info = query("""  SELECT P.id_pertandingan, T.tim_a, T.tim_b, S.nama stadium, P.start_datetime
               FROM D02.PERTANDINGAN P 
               NATURAL JOIN 
               (SELECT A.id_pertandingan, A.nama_tim tim_a, B.nama_tim tim_b 
               FROM D02.TIM_PERTANDINGAN A JOIN D02.TIM_PERTANDINGAN B 
               ON A.id_pertandingan = B.id_pertandingan 
               WHERE A.nama_tim < B.nama_tim) T 
               JOIN D02.STADIUM S ON S.id_stadium = P.stadium 
               WHERE P.id_pertandingan NOT IN (SELECT id_pertandingan FROM D02.RAPAT)""")

    context = {"pertandingan": info}

    if request.method == "POST":
        request.session['pidrapat'] = request.POST.get('mulai')
        return redirect("/mulai_rapat/rapat")

    return render(request, 'mulai_rapat.html', context)


def rapat(request):
    pid = request.session.get('pidrapat')

    if request.COOKIES.get('role') != 'Panitia':
        return redirect('/dashboard')

    pertandingan = query(f"""SELECT A.nama_tim tim_a, B.nama_tim tim_b
                           FROM D02.TIM_PERTANDINGAN A JOIN D02.TIM_PERTANDINGAN B 
                           ON A.id_pertandingan = B.id_pertandingan 
                           WHERE A.nama_tim < B.nama_tim AND A.id_pertandingan= '{pid}'""")

    context = {"pertandingan": pertandingan}

    if request.method == "POST":
        user = request.COOKIES.get('username')
        panitia = query(f"SELECT id_panitia FROM PANITIA WHERE username = '{user}'")[0]['id_panitia']

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        manajer_a = query(f"""SELECT id_manajer::text
                          FROM D02.tim_manajer
                          WHERE nama_tim =  '{pertandingan[0]['tim_a']}'""")[0]['id_manajer']

        manajer_b = query(f"""SELECT id_manajer::text
                          FROM D02.tim_manajer
                          WHERE nama_tim =  '{pertandingan[0]['tim_b']}'""")[0]['id_manajer']

        isi = request.POST.get("isi")
        query("INSERT INTO RAPAT VALUES ('{0}','{1}','{2}','{3}','{4}','{5}');"
              .format(pid, date, panitia, manajer_a, manajer_b, isi))

        return redirect("/dashboard")

    return render(request, 'rapat.html', context)

