import psycopg2
from psycopg2 import Error

from resources.db_creds import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_PORT,
)

def get_postgres_version() -> str:
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        return result[0]

    except Error as error:
        raise error


    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    print(connect_to_postgres())