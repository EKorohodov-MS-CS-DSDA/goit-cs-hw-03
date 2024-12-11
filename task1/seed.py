import psycopg2
import faker
from connect import DB_CONFIG

MAX_TASKS_PER_USER = 5
MAX_USERS = 30

STATUSES = ["new", "in progress", "completed"]


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


def generate_tasks():
    fake = faker.Faker()
    tasks = []
    for _ in range(MAX_TASKS_PER_USER):
        task = {
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": fake.random.randint(1, len(STATUSES)),
        }
        tasks.append(task)
    return tasks

def generate_users():
    fake = faker.Faker()
    users = []
    for _ in range(MAX_USERS):
        user = {
            "name": fake.name(),
            "email": fake.email(),
            "tasks": []
        }
        users.append(user)
    return users


if __name__ == "__main__":
    connection = database_connect()

    users = generate_users()
    for user in users:
        tasks = generate_tasks()
        user["tasks"] = tasks

    with connection.cursor() as cursor:
        for idx, status in enumerate(STATUSES, start=1):
            cursor.execute(
                "INSERT INTO status (id, name) VALUES (%s, %s)",
                (idx, status)
            )

        for user in users:
            cursor.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id",
                (user["name"], user["email"])
            )
            user_id = cursor.fetchone()[0]
            for task in user["tasks"]:
                cursor.execute(
                    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (task["title"], task["description"], task["status_id"], user_id)
                )

    connection.commit()
