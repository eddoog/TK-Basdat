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
    -- Pelatih
    CREATE OR REPLACE FUNCTION validate_coach_assignment()
    RETURNS TRIGGER AS 
    $$
        DECLARE
        coach_count INTEGER;
        BEGIN
        -- Count the number of coaches for the specified team
        SELECT COUNT(*) INTO coach_count
        FROM pelatih
        WHERE nama_tim = NEW.nama_tim;

        IF coach_count = 0 THEN
            -- No coaches yet, allow the new coach to be registered
            RETURN NEW;
        ELSIF coach_count = 1 THEN
            -- Check if the new coach has a different specialization
            IF EXISTS (
                SELECT 1
                FROM spesialisasi_pelatih
                WHERE id_pelatih = NEW.id_pelatih
                    AND spesialisasi IN (
                    SELECT spesialisasi
                    FROM spesialisasi_pelatih
                    WHERE id_pelatih IN (
                        SELECT id_pelatih
                        FROM pelatih
                        WHERE nama_tim = NEW.nama_tim
                    )
                    )
            ) THEN
            -- New coach has the same specialization as the existing coach, raise an exception
            RAISE EXCEPTION 'Pelatih baru memiliki spesialisasi yang sama dengan pelatih lain di tim';
            END IF;
        ELSIF coach_count = 2 THEN
            -- Already 2 coaches, raise an exception
            RAISE EXCEPTION 'Tim sudah memiliki dua pelatih';
        END IF;

        RETURN NEW;
        END;
    $$ 
    LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER validate_coach_assignment_trigger
    BEFORE INSERT OR UPDATE ON Pelatih
    FOR EACH ROW
    EXECUTE FUNCTION validate_coach_assignment();

    -- Kapten
    CREATE OR REPLACE FUNCTION change_captain()
    RETURNS TRIGGER AS 
    $$
    BEGIN
        IF NEW.is_captain THEN
            UPDATE PEMAIN
            SET is_captain = FALSE
            WHERE nama_tim = NEW.nama_tim AND is_captain = TRUE;
        END IF;
        RETURN NEW;
    END;
    $$ 
    LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER change_captain_trigger
    BEFORE INSERT OR UPDATE ON PEMAIN
    FOR EACH ROW
    EXECUTE FUNCTION change_captain();


-- CRU Peminjaman Stadium & CR Mulai Rapat (Merah)

-- CRUD Pembuatan Pertandingan (Biru)

-- CRD Mulai Pertandingan & R Manage Pertandingan (Ungu)

-- CR Pembelian Tiket & R List Pertandingan &  R History Rapat (Kuning)