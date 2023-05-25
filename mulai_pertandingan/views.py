from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
def mulai_pertandingan(request):
    return render(request, 'mulai_pertandingan.html')

def pilih_peristiwa(request):
    return render(request, 'pilih_peristiwa.html')
=======
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
# from authenticate.decorators import login_required



def funct_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
# @login_required
def mulai_pertandingan(request):
    # role = request.session.get("role", None)
    # if role != "panitia":
    #     return HttpResponse("Anda tidak memiliki akses ke halaman ini")
    
    cursor = connection.cursor()
    
    cursor.execute(
        f"SELECT id_pertandingan, tim_1, tim_2 FROM ( SELECT t1.id_pertandingan as id_pertandingan, t1.nama_tim AS tim_1, t2.nama_tim AS tim_2, ROW_NUMBER() OVER (PARTITION BY t1.id_pertandingan ORDER BY t1.nama_tim) AS rn FROM d02.tim_pertandingan t1 JOIN d02.tim_pertandingan t2 ON t1.id_pertandingan = t2.id_pertandingan WHERE t1.nama_tim < t2.nama_tim) AS subquery WHERE rn = 1 ORDER BY tim_1;"
    )

    tim = funct_fetchall(cursor)
    tableTim = []
    if tim != []:
        cursor.execute(
            f"SELECT id_pertandingan, tim_1, tim_2 FROM ( SELECT t1.id_pertandingan,  t1.nama_tim AS tim_1, t2.nama_tim AS tim_2, ROW_NUMBER() OVER (PARTITION BY t1.id_pertandingan ORDER BY t1.nama_tim) AS rn FROM d02.tim_pertandingan t1 JOIN d02.tim_pertandingan t2 ON t1.id_pertandingan = t2.id_pertandingan WHERE t1.nama_tim < t2.nama_tim) AS subquery WHERE rn = 1 ORDER BY tim_1;"
        )
        tim = cursor.fetchall()
        tableTim = [
            {
                "tim_1": tim_tanding[1],
                "tim_2": tim_tanding[2],
                "id_pertandingan":tim_tanding[0]
            }
            for tim_tanding in tim
        ]
    context = {'tim_mp': tableTim}
    
    cursor.close()

    print(context)
    return render(request, 'mulai_pertandingan.html', context)

@csrf_exempt
def pilih_peristiwa(request, id_pertandingan, nama_tim): #MASIH ERROR
    cursor = connection.cursor()
    cursor.execute(f"SET SEARCH_PATH TO d02")

    cursor.execute(
        f"SELECT P.ID_Pemain as id, CONCAT(P.nama_depan,' ',P.nama_belakang) AS nama_pemain FROM d02.PEMAIN P WHERE P.nama_tim='{nama_tim}';"
    )
    pemain_datas = cursor.fetchall()
    pemain = [{'id': pemain_data[0], 'name': pemain_data[1].strip()} for pemain_data in pemain_datas]

    context = {'dropdown_pemain': pemain, 'nama_tim': nama_tim, 'id_pertandingan' : id_pertandingan}
    
    if request.method == "POST":
        #Logic untuk update peristiwa : 
        pemain = request.POST.get('pemain')
        peristiwa = request.POST.get('peristiwa')
        waktu = request.POST.get('waktu')
        print(waktu, pemain, peristiwa)
        if pemain == "None" and peristiwa == "None" or waktu == "None":
            return redirect("mulai_pertandingan:mulai_pertandingan")
        #     messages.error(request, "Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.")
        # else:
        try:
            # Handle the exception
            # You can log the error, display an error message, or take any other necessary action
            cursor.callproc('insert_peristiwa', [id_pertandingan, waktu, peristiwa, pemain])
            messages.success(request, f"Berhasil menambahkan peristiwa baru !")
            return redirect("mulai_pertandingan:mulai_pertandingan")
        except Exception as e:
            cursor.execute(
                f"SELECT P.ID_Pemain as id, CONCAT(P.nama_depan,' ',P.nama_belakang) AS nama_pemain FROM d02.PEMAIN P WHERE P.ID_pemain='{pemain}';"
            )

            current_pemain = cursor.fetchall()
            
            messages.error(request, f"Pemain dengan nama {current_pemain[0][1]} sudah mendapatkan kartu merah dan tidak dapat lagi menambah peristiwa baru !")
                # Generate the URL with parameters using reverse()

        
            url = reverse('mulai_pertandingan:pilih_peristiwa', kwargs={'id_pertandingan': id_pertandingan, 'nama_tim': nama_tim})
            
            # Redirect to the generated URL
            return redirect(url)
        
        
    cursor.close()
    
    return render(request, 'pilih_peristiwa.html',context)



>>>>>>> 01ac25c1ccd1cc8b99b837a5a1d995121080f1c4
