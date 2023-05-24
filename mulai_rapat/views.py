from django.shortcuts import render, redirect
from django.db import connection
import datetime

def mulai_rapat(request):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")
        cursor.execute("SELECT P.id_pertandingan, T.tim_a, T.tim_b, S.nama stadium, P.start_datetime \
                       FROM D02.PERTANDINGAN P \
                       NATURAL JOIN \
                       (SELECT A.id_pertandingan, A.nama_tim tim_a, B.nama_tim tim_b \
                       FROM D02.TIM_PERTANDINGAN A JOIN D02.TIM_PERTANDINGAN B \
                       ON A.id_pertandingan = B.id_pertandingan \
                       WHERE A.nama_tim < B.nama_tim) T \
                       JOIN D02.STADIUM S ON S.id_stadium = P.stadium \
                       WHERE P.id_pertandingan NOT IN (SELECT id_pertandingan FROM D02.RAPAT)")
        info_pertandingan = cursor.fetchall()
        response["pertandingan"] = info_pertandingan

        if request.method == "POST":
            return redirect("/mulai_rapat/rapat/" + request.POST.get("mulai"))

    return render(request, 'mulai_rapat.html', response)


def rapat(request, pid):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")
        cursor.execute("""SELECT A.nama_tim tim_a, B.nama_tim tim_b
                           FROM D02.TIM_PERTANDINGAN A JOIN D02.TIM_PERTANDINGAN B 
                           ON A.id_pertandingan = B.id_pertandingan 
                           WHERE A.nama_tim < B.nama_tim AND A.id_pertandingan= '{0}'""".format(pid))
        pertandingan = cursor.fetchall()
        response["pertandingan"] = pertandingan

        if request.method == "POST":
            # TODO
            panitia = "588a11d3-6397-4fa0-8d48-7da97cd59538"

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""SELECT id_manajer::text
                              FROM D02.tim_manajer
                              WHERE nama_tim =  '{0}'""".format(pertandingan[0][0]))
            manajer_a = cursor.fetchall()[0][0]

            cursor.execute("""SELECT id_manajer::text
                              FROM D02.tim_manajer
                              WHERE nama_tim =  '{0}'""".format(pertandingan[0][1]))
            manajer_b = cursor.fetchall()[0][0]

            cursor.execute("INSERT INTO RAPAT VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')"
                           .format(pid, date, panitia, manajer_a, manajer_b, request.POST.get("isi")))

            return redirect("/mulai_rapat")

    return render(request, 'rapat.html', response)

