import psycopg2
from connect import DB_CONFIG

# Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
sql_all_tasks_by_user_id = """
    SELECT *
    FROM tasks
    WHERE user_id = %s
    """

# Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
sql_tasks_by_status = """
    SELECT *
    FROM tasks
    JOIN status ON tasks.status_id = status.id
    WHERE status.name = %s
    """

# Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
sql_update_task_status = """
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s
    """

# Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
sql_users_without_tasks = """
    SELECT *
    FROM users
    WHERE id NOT IN (
        SELECT user_id
        FROM tasks
    )
    """

# Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
sql_add_task = """
    INSERT INTO tasks (user_id, title, description, status_id)
    VALUES (%s, %s, %s, (SELECT id FROM status WHERE name = %s))
    """

# Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
sql_unfinished_tasks = """
    SELECT *
    FROM tasks
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """

# Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
sql_delete_task = """
    DELETE FROM tasks
    WHERE id = %s
    """

# Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
sql_users_by_email = """
    SELECT *
    FROM users
    WHERE email LIKE %s
    """

# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
sql_update_user_name = """
    UPDATE users
    SET fullname = %s
    WHERE id = %s
    """

# Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
sql_tasks_by_status_count = """
    SELECT status_id, COUNT(*)
    FROM tasks
    GROUP BY status_id
    """

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
sql_tasks_by_email_domain = """
    SELECT *
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE users.email LIKE %s
    """

# Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
sql_tasks_without_description = """
    SELECT *
    FROM tasks
    WHERE description IS NULL OR description = ''
    """

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
sql_inprogress_tasks_by_user_id = """
    SELECT tasks.*, users.fullname AS user_name
    FROM tasks
    INNER JOIN users ON tasks.user_id = users.id
    WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress')
    """

# Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
sql_users_with_tasks_count = """
    SELECT users.*, COUNT(tasks.id) AS task_count
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.id
    """

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

def database_execute(sql, params):
    try:
        conn = database_connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        yield cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        if conn:
            conn.rollback()
    finally:
        cur.close()
        conn.close()

def print_query_result(result):
    if not result:
        print("The query provides no printable results.")
        return
    for row in result:
        print(row)

if __name__ == "__main__":
    # Отримати всі завдання певного користувача.
    print_query_result( database_execute(sql_all_tasks_by_user_id, (5,)))

    # Вибрати завдання за певним статусом.
    print_query_result( database_execute(sql_tasks_by_status, ('in progress',)))

    # Оновити статус конкретного завдання.
    print_query_result( database_execute(sql_update_task_status, ('in progress', 10)))

    # Отримати список користувачів, які не мають жодного завдання.
    print_query_result( database_execute(sql_users_without_tasks, ()))

    # Додати нове завдання для конкретного користувача.
    print_query_result( database_execute(sql_add_task, (5, 'New task', '', 'in progress')))

    # Отримати всі завдання, які ще не завершено.
    print_query_result( database_execute(sql_unfinished_tasks, ()))

    # Видалити конкретне завдання.
    print_query_result( database_execute(sql_delete_task, (4,)))

    # Знайти користувачів з певною електронною поштою.
    print_query_result( database_execute(sql_users_by_email, ('%@example.com',)))

    # Оновити ім'я користувача.
    print_query_result( database_execute(sql_update_user_name, ('John Doe', 5)))

    # Отримати кількість завдань для кожного статусу.
    print_query_result( database_execute(sql_tasks_by_status_count, ()))

    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    print_query_result( database_execute(sql_tasks_by_email_domain, ('%@example.com',)))

    # Отримати список завдань, що не мають опису.
    print_query_result( database_execute(sql_tasks_without_description, ()))

    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'.
    print_query_result( database_execute(sql_inprogress_tasks_by_user_id, ()))

    # Отримати користувачів та кількість їхніх завдань.
    print_query_result( database_execute(sql_users_with_tasks_count, ()))
