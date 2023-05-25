from collections import namedtuple
import psycopg2
from psycopg2 import Error, errors
from psycopg2.extras import RealDictCursor
from utils.db_utils import fetch_convert_to_dict

try:
    connection = psycopg2.connect(user="postgres",
                                  password='Bu7rxUgIh1WyT9N6Rnnt',
                                  host='containers-us-west-179.railway.app',
                                  port='6087',
                                  database="railway")

    connection.autocommit = True
    cursor = connection.cursor()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def query(query_str: str):
    hasil = []
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO D02")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                hasil = fetch_convert_to_dict(cursor)
            else:
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:
            hasil = e

    return hasil
