from django.shortcuts import render, redirect
from django.db import connection



# Create your views here.
def peminjaman_stadium(request):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")
        cursor.execute("SELECT nama, start_datetime, end_datetime FROM PEMINJAMAN NATURAL JOIN STADIUM")
        response["history_peminjaman"] = cursor.fetchall()
    print(response)

    # TODO: manager role
    return render(request, 'peminjaman-stadium.html', response)


def pesan_stadium(request):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")
        cursor.execute("SELECT id_stadium, nama FROM STADIUM")
        response["stadiums"] = cursor.fetchall()

        if request.method == "POST":
            url = "/peminjaman_stadium/pesan/pilih_waktu/" \
                  + request.POST.get("stadium") \
                  + "/" + request.POST.get("tanggal")
            return redirect(url)

    return render(request, 'pesan-stadium.html', response)


def pilih_waktu_stadium(request, sid, date):
    response = {}

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")

        if request.method == "POST":
            # TODO
            m_id = '0c697e4f-8563-46c3-9708-0ba88039e51d'

            time = request.POST.get("time").strip("()'").split("', '")
            start_datetime = date + " " + time[0]
            end_datetime = date + " " + time[1]

            cursor.execute("INSERT INTO D02.PEMINJAMAN VALUES ('{0}','{1}','{2}','{3}')"
                           .format(m_id, start_datetime, end_datetime, sid))

            return redirect("/peminjaman_stadium")

        query = """
            SELECT *
            FROM (
                SELECT '06:00:00' start, '09:00:00' end UNION 
                SELECT '10:00:00', '13:00:00' UNION 
                SELECT '14:00:00', '17:00:00' UNION 
                SELECT '18:00:00', '21:00:00'
            ) TEMP 
            WHERE (TEMP.start, TEMP.end) 
            NOT IN (
                SELECT start_datetime::time::varchar, end_datetime::time::varchar 
                FROM d02.PEMINJAMAN
                WHERE start_datetime::date = '{0}'
                AND id_stadium = '{1}'
            )
            ORDER BY start
        """.format(date, sid)

        cursor.execute(query)
        response["available_time"] = cursor.fetchall()

        cursor.execute("SELECT nama FROM D02.STADIUM WHERE id_stadium = '{0}'".format(sid))
        response["stadium_name"] = cursor.fetchall()[0][0]

    return render(request, 'pilih-waktu-stadium.html', response)
