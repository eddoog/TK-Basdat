from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.query import query
from utils.users import check_username, check_role

# Create your views here.


def peminjaman_stadium(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    m_user = request.COOKIES.get('username')
    m_id = query(f"SELECT id_manajer FROM MANAJER WHERE username = '{m_user}'")[
        0]['id_manajer']

    hst = query(f"""SELECT id_manajer, nama, start_datetime, row_number() over (ORDER BY start_datetime)
                    FROM PEMINJAMAN NATURAL JOIN STADIUM 
                    WHERE id_manajer = '{m_id}'
                    """)

    context = {'history_peminjaman': hst}
    print(hst)

    if request.method == "POST":
        request.session["mid"] = str(m_id)

        date = hst[int(request.POST.get("index"))-1]['start_datetime']

        request.session["tgl"] = str(date)
        return redirect("/peminjaman_stadium/edit")

    return render(request, 'peminjaman-stadium.html', context)


def pesan_stadium(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    context = {'stadiums': query("SELECT id_stadium, nama FROM STADIUM")}

    if request.method == "POST":

        sid = request.POST.get("stadium")
        tgl = request.POST.get("tanggal")

        m_user = request.COOKIES.get('username')
        m_id = query(f"SELECT id_manajer FROM MANAJER WHERE username = '{m_user}'")[
            0]['id_manajer']

        res = query(
            f"INSERT INTO D02.PEMINJAMAN VALUES ('{m_id}','{tgl}','{tgl}','{sid}')")
        res = f"{res}"
        if res != "1":

            if res.startswith("Stadium"):
                context["message"] = res.split("\n")[0]

            elif res.startswith("duplicate"):
                context["message"] = "Anda sudah memiliki peminjaman stadium di tanggal tersebut"

            return render(request, 'pesan-stadium.html', context)

        return redirect("/peminjaman_stadium")

    return render(request, 'pesan-stadium.html', context)


def edit(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Manajer'):
        return redirect('/dashboard')

    date = request.session.get("tgl")
    context = {'stadiums': query("SELECT id_stadium, nama FROM STADIUM"),
               'tanggal': f"{date[8:]}/{date[5:7]}/{date[0:4]}"}

    if request.method == "POST":

        m_user = request.COOKIES.get('username')
        m_id = query(f"SELECT id_manajer FROM MANAJER WHERE username = '{m_user}'")[
            0]['id_manajer']
        sid = request.POST.get("stadium")

        res = str(query(
            f"UPDATE D02.PEMINJAMAN SET id_stadium = '{sid}' WHERE id_manajer = '{m_id}' AND start_datetime = '{date}'"))
        print(res)
        if res != "1":
            if res.startswith("Stadium"):
                context["message"] = res.split("\n")[0]

            elif res.startswith("duplicate"):
                context["message"] = "Anda sudah memiliki peminjaman stadium di tanggal tersebut"

            return render(request, 'edit-pinjaman.html', context)

        return redirect("/peminjaman_stadium")

    return render(request, 'edit-pinjaman.html', context)

# def pilih_waktu_stadium(request):
#     if request.COOKIES.get('role') != 'Manajer':
#         return redirect('/dashboard')
#
#     sid = request.COOKIES.get('pinjamstadium')
#     tanggal = request.COOKIES.get('tanggalpinjam')
#
#     if request.method == "POST":
#         m_user = request.COOKIES.get('username')
#         m_id = query(f"SELECT id_manajer FROM MANAJER WHERE username = '{m_user}'")[0]['id_manajer']
#
#         time = request.POST.get("time").strip("()'").split("', '")
#         start_datetime = tanggal + " " + time[0]
#         end_datetime = tanggal + " " + time[1]
#
#         query(f"INSERT INTO D02.PEMINJAMAN VALUES ('{m_id}','{start_datetime}','{end_datetime}','{sid}')")
#
#         return redirect("/peminjaman_stadium")
#
#     times = query(f"""
#         SELECT *
#         FROM (
#             SELECT '06:00:00' start, '09:00:00' end UNION
#             SELECT '10:00:00', '13:00:00' UNION
#             SELECT '14:00:00', '17:00:00' UNION
#             SELECT '18:00:00', '21:00:00'
#         ) TEMP
#         WHERE (TEMP.start, TEMP.end)
#         NOT IN (
#             SELECT start_datetime::time::varchar, end_datetime::time::varchar
#             FROM d02.PEMINJAMAN
#             WHERE start_datetime::date = '{tanggal}'
#             AND id_stadium = '{sid}'
#         )
#         ORDER BY start
#     """)
#
#     s_name = query(f"SELECT nama FROM D02.STADIUM WHERE id_stadium = '{sid}'")[0]['nama']
#
#     response = {'available_times': times, 'stadium_name': s_name}
#
#     return render(request, 'pilih-waktu-stadium.html', response)
