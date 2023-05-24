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

-- CRUD Pembuatan Pertandingan (Biru)

-- CRD Mulai Pertandingan & R Manage Pertandingan (Ungu)

-- CR Pembelian Tiket & R List Pertandingan &  R History Rapat (Kuning)