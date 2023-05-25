from queue import Empty
from django.shortcuts import render
from django.db import connection
# Create your views here.

def funct_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def pertandingan_belum_lengkap(request):
    cursor = connection.cursor()
    cursor.execute(f" SELECT * FROM d02.PERTANDINGAN")
    pertandingan = funct_fetchall(cursor)
    if pertandingan is Empty:
        cursor.close()
        return render(request, 'pertandingan_belum_lengkap.html')

def pertandingan_group_stage_pertama(request):
    cursor = connection.cursor()
    cursor.execute(f"SET SEARCH_PATH TO d02")
    cursor.execute("""
       SELECT
            p.ID_Pertandingan AS id_pertandingan,
            t1.Nama_Tim AS tim_1,
            t2.Nama_Tim AS tim_2,
            (
                SELECT
                    json_agg(json_build_object(
                        'nama_pemain', pm1.Nama_Depan || ' ' || pm1.Nama_Belakang,
                        'jenis', ps1.Jenis,
                        'waktu', ps1.Datetime
                    ))
                FROM
                    Pemain pm1
                    JOIN Peristiwa ps1 ON ps1.ID_Pemain = pm1.ID_Pemain
                WHERE
                    ps1.ID_Pertandingan = p.ID_Pertandingan
                    AND pm1.Nama_Tim = t1.Nama_Tim
            ) AS peristiwa_tim_1,
            (
                SELECT
                    json_agg(json_build_object(
                        'nama_pemain', pm2.Nama_Depan || ' ' || pm2.Nama_Belakang,
                        'jenis', ps2.Jenis,
                        'waktu', ps2.Datetime
                    ))
                FROM
                    Pemain pm2
                    JOIN Peristiwa ps2 ON ps2.ID_Pemain = pm2.ID_Pemain
                WHERE
                    ps2.ID_Pertandingan = p.ID_Pertandingan
                    AND pm2.Nama_Tim = t2.Nama_Tim
            ) AS peristiwa_tim_2,
            p.Start_Datetime AS start_date,
            CASE
                WHEN tp1.Skor > tp2.Skor THEN t1.Nama_Tim
                WHEN tp1.Skor < tp2.Skor THEN t2.Nama_Tim
                ELSE 'Draw'
            END AS pemenang
        FROM
            Pertandingan p
            JOIN Tim_Pertandingan tp1 ON tp1.ID_Pertandingan = p.ID_Pertandingan
            JOIN Tim t1 ON t1.Nama_Tim = tp1.Nama_Tim
            JOIN Tim_Pertandingan tp2 ON tp2.ID_Pertandingan = p.ID_Pertandingan
            JOIN Tim t2 ON t2.Nama_Tim = tp2.Nama_Tim
        WHERE t1.Nama_Tim < t2.Nama_Tim;
    """)

    rows = cursor.fetchall()

    pertandingan_data = []
    for row in rows:
        pertandingan = {
            'id': row[0],
            'tim_1': row[1],
            'tim_2': row[2],
            'peristiwa_tim_1': row[3],
            'peristiwa_tim_2': row[4],
            'waktu': row[5],
            'pemenang':row[6]
        }
        pertandingan_data.append(pertandingan)


    context = {'pertandingan_data':pertandingan_data}
  
    return render(request,'group_stage_pertama.html',context)

def peristiwa_tim(request):
    return render(request,'peristiwa_tim.html')

def pertandingan_group_stage_kedua(request):
    return render(request,'group_stage_kedua.html')

def playoff(request):
    return render(request,'playoff_stage.html')

def akhir_musim(request):
    return render(request,'akhir_musim.html')