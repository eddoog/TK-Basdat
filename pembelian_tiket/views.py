from django.shortcuts import render, redirect
from django.db import connection
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from utils.users import check_username, check_role


def pesan_tiket(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Penonton'):
        return redirect('/dashboard')

    if request.method == "POST":

        username = request.COOKIES.get('username')

        with connection.cursor() as cursor:
            cursor.execute("""
                                SELECT P.ID_penonton 
                                FROM D02.penonton P, D02.user_system U 
                                WHERE U.username = %s AND P.username = U.username;
                                 """, [username])

            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        uuid_penonton = data[0]['id_penonton']
        id_pertandingan = request.session.get('pertandingan')
        jenis_tiket = request.POST.get('tiket')
        jenis_pembayaran = request.POST.get('pembayaran')
        nomor_receipt = generate_receipt()

        # print(uuid_penonton)
        # print(id_pertandingan)
        # print(jenis_tiket)
        # print(jenis_pembayaran)
        # print(nomor_receipt)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO D02.PEMBELIAN_TIKET VALUES (%s, %s, %s, %s, %s)
                """, [nomor_receipt, uuid_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan])

        return HttpResponse('Ticket purchased successfully!')
    else:

        return HttpResponse(status=405)


def generate_receipt():
    with connection.cursor() as cursor:
        cursor.execute("""
                            SELECT COUNT(*) as Total_tuples
                            FROM D02.PEMBELIAN_TIKET PT;
                                """)

        columns = [col[0] for col in cursor.description]

        data = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    jumlah_receipt = (data[0]['total_tuples'])
    receipt = jumlah_receipt + 1

    return receipt


def beli_tiket(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Penonton'):
        return redirect('/dashboard')

    if request.method == 'POST':
        pertandingan = request.POST.get('id_pertandingan')
        request.session['pertandingan'] = pertandingan

        # Do further processing with the captured values (e.g., validation, database operations)
        print(f"Selected Pertandingan: {pertandingan}")

        # Return the rendered template or redirect to another page
        return render(request, 'beli_tiket.html')

    # Handle other HTTP methods if needed
    else:
        return HttpResponseNotAllowed(['GET'])


def pilih_pertandingan(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Penonton'):
        return redirect('/dashboard')

    if request.method == 'POST':
        response = redirect("/pembelian_tiket/pilih_pertandingan")
        stadium = request.POST.get('stadium')
        date = request.POST.get('date-field')

        request.session['stadium'] = stadium
        request.session['date'] = date

        # Do further processing with the captured values (e.g., validation, database operations)

        print(f"Selected Stadium: {stadium}")
        print(f"Selected Date: {date}")

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id_pertandingan, string_agg(nama_tim, ' </td><td> ') as tim_bertanding
                FROM D02.pertandingan p
                JOIN D02.stadium s ON p.stadium = s.id_stadium
                JOIN D02.tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                WHERE s.nama = %s AND p.start_datetime = %s
                GROUP BY p.id_pertandingan;
                 """, [stadium, date])

            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            # print(data)

        context = {'data': data}

        # Return the rendered template or redirect to another page
        return render(request, 'pilih_pertandingan.html', context)

    # Handle other HTTP methods if needed
    else:
        return HttpResponseNotAllowed(['GET'])


def pilih_stadium(request):
    username = check_username(request)
    if (username is None):
        return redirect('/')

    role = check_role(request)
    if (role is None):
        return redirect('/')

    if (role != 'Penonton'):
        return redirect('/dashboard')
    if request.method == 'GET':
        # print('Menampilkan Stadium')
        # print(request.session['akun_pengguna'])

        with connection.cursor() as cursor:
            cursor.execute("""
                                SELECT nama
                                FROM D02.stadium
                                """)
            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            # print(data)

        context = {'data': data}

        return render(request, 'pilih_stadium.html', context)
