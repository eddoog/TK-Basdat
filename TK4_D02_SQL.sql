-- Fitur wajib
    -- Navbar login password
    CREATE OR REPLACE FUNCTION check_duplicate_username()
    RETURNS TRIGGER AS 
    $$
    BEGIN
        IF EXISTS(SELECT 1 FROM User_System WHERE Username = NEW.Username) THEN
            RAISE EXCEPTION 'Username has already been used';
        END IF;
        RETURN NEW;
    END;
    $$ 
    LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER check_duplicate_username_trigger
    BEFORE INSERT ON User_System
    FOR EACH ROW
    EXECUTE FUNCTION check_duplicate_username();

    -- Dashboard

    -- CRU Pengguna

-- CRU Mengelola tim (Hijau)

-- CRU Peminjaman Stadium & CR Mulai Rapat (Merah)
CREATE OR REPLACE FUNCTION check_stadium_availability() RETURNS trigger AS
$$
BEGIN
    IF EXISTS (
        SELECT *
        FROM (
                 SELECT start_datetime, end_datetime, stadium
                 FROM D02.PERTANDINGAN
                 UNION SELECT start_datetime, end_datetime, id_stadium
                 FROM D02.PEMINJAMAN
             ) temp
        WHERE temp.stadium = NEW.id_stadium
          AND start_datetime <= NEW.end_datetime
          AND end_datetime >= NEW.start_datetime
    )
    THEN
        RAISE EXCEPTION 'Stadium yang dipilih tidak tersedia pada tanggal yang tersebut';
    END IF;
    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER stadium_availability
    BEFORE INSERT OR UPDATE ON D02.PEMINJAMAN
    FOR EACH ROW
EXECUTE FUNCTION check_stadium_availability();

-- CRUD Pembuatan Pertandingan (Biru)

-- CRD Mulai Pertandingan & R Manage Pertandingan (Ungu)

-- CR Pembelian Tiket & R List Pertandingan &  R History Rapat (Kuning)