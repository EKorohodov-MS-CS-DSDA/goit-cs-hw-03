import psycopg2
from connect import DB_CONFIG

def database_connect():
    """
    Connect to PostgreSQL database and return a connection object.

    :return: connection object
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


sql_create_table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE
        );
    """

sql_create_table_status = """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE
        );
    """

sql_create_table_tasks = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description     TEXT,
            status_id INTEGER NOT NULL,
            FOREIGN KEY (status_id) REFERENCES status (id),
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
                ON DELETE CASCADE
        );
    """

sql_drop_table_users = """
        DROP TABLE IF EXISTS users CASCADE;
    """

sql_drop_table_status = """
        DROP TABLE IF EXISTS status CASCADE;
    """

sql_drop_table_tasks = """
        DROP TABLE IF EXISTS tasks CASCADE;
    """

def run_sql_script(connection, sql_script):
    with connection.cursor() as cursor:
        cursor.execute(sql_script)
    connection.commit()

if __name__ == '__main__':
    connection = database_connect()

    # Drop and create tables
    run_sql_script(connection, sql_drop_table_users)
    run_sql_script(connection, sql_drop_table_status)
    run_sql_script(connection, sql_drop_table_tasks)

    run_sql_script(connection, sql_create_table_users)
    run_sql_script(connection, sql_create_table_status)
    run_sql_script(connection, sql_create_table_tasks)

    connection.close()
