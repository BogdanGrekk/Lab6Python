import pymysql
import random
from datetime import date, timedelta

def insert_data():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='pasfordb',
        db='LRaMDdatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    names = ["Олег", "Михайло", "Василь", "Олексій", "Дмитро", "Сергій", "Андрій", "Павло", "Іван"]
    surnames = ["Петров", "Іванов", "Сидоренко", "Козлов", "Мельник", "Шевченко", "Коваленко", "Мороз", "Дубов"]
    middle_names = ["Олександрович", "Михайлович", "Васильович", "Олексійович", "Дмитрович", "Сергійович", "Андрійович", "Павлович", "Іванович"]

    try:
        with connection.cursor() as cursor:
            locomotives = [
                (f"L00{i}", random.choice(["Фастів", "Козятин", "П’ятихатки"]), random.choice(["cargo", "passenger"]), random.randint(1990, 2020)) for i in range(1, 10)
            ]
            cursor.executemany('''
                INSERT INTO Locomotives (registration_number, depot, locomotive_type, year_of_production)
                VALUES (%s, %s, %s, %s)
            ''', locomotives)

            # Запит до БД, щоб отримати існуючі ID локомотивів
            cursor.execute("SELECT locomotive_id FROM Locomotives")
            locomotive_ids = [item["locomotive_id"] for item in cursor.fetchall()]

            brigades = [
                (i, f"+38050{i}234567") for i in range(1, 4)
            ]
            cursor.executemany('''
                INSERT INTO Brigades (brigade_number, phone)
                VALUES (%s, %s)
            ''', brigades)

            workers = []
            for i in range(1, 10):
                is_leader = False
                if i % 3 == 0:
                    is_leader = True
                workers.append((
                    random.choice(surnames),
                    random.choice(names),
                    random.choice(middle_names),
                    (i - 1) // 3 + 1,
                    is_leader,
                    date(1980, 1, 1) + timedelta(days=random.randint(0, 14600))
                ))
            cursor.executemany('''
                INSERT INTO Workers (last_name, first_name, middle_name, brigade_number, is_brigade_leader, birth_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', workers)

            repairs = [
                (random.choice(locomotive_ids), random.choice(["current", "maintenance", "unscheduled"]), date(2020, 1, 1) + timedelta(days=random.randint(0, 600)), random.randint(1, 30), random.uniform(100, 500), random.randint(1, 3)) for i in range(1, 12)
            ]
            cursor.executemany('''
                INSERT INTO Repairs (locomotive_id, repair_type, start_date, days_required, daily_repair_cost, brigade_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', repairs)

            connection.commit()

    finally:
        connection.close()

if __name__ == "__main__":
    insert_data()
