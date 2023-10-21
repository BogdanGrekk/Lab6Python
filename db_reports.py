import pymysql

def fetch_data_and_structure():
    # Параметри підключення до бази даних
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='pasfordb',
        db='LRaMDdatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Отримання списку таблиць
            cursor.execute("SHOW TABLES")
            tables = [table['Tables_in_LRaMDdatabase'] for table in cursor.fetchall()]

            for table in tables:
                print(f"\nTable: {table}\n{'='*40}")

                # Виведення структури таблиці
                cursor.execute(f"DESCRIBE {table}")
                structure = cursor.fetchall()
                print("Structure:")
                for column in structure:
                    print(column)

                # Виведення даних з таблиці
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                print("\nData:")
                for row in rows:
                    print(row)

            # Виведення результатів запитів
            print("\nResults of Queries\n" + "="*40)

            # Запит 1
            cursor.execute("SELECT * FROM Locomotives WHERE locomotive_type='cargo' ORDER BY year_of_production")
            locomotives = cursor.fetchall()
            print("\nCargo Locomotives sorted by production year:")
            for loco in locomotives:
                print(loco)

            # Запит 2
            cursor.execute("SELECT locomotive_id, DATE_ADD(start_date, INTERVAL days_required DAY) as end_date FROM Repairs")
            end_dates = cursor.fetchall()
            print("\nEnd date for each locomotive repair:")
            for end_date in end_dates:
                print(end_date)

            # Запит 3
            cursor.execute("SELECT brigade_number, COUNT(*) as repair_count FROM Repairs GROUP BY brigade_number")
            brigade_counts = cursor.fetchall()
            print("\nNumber of repairs by each brigade:")
            for brigade_count in brigade_counts:
                print(brigade_count)

            # Запит 4
            cursor.execute("SELECT locomotive_id, SUM(daily_repair_cost * days_required) as total_cost FROM Repairs GROUP BY locomotive_id")
            total_costs = cursor.fetchall()
            print("\nTotal repair cost for each locomotive:")
            for total_cost in total_costs:
                print(total_cost)

            # Запит 5
            cursor.execute("SELECT brigade_number, repair_type, COUNT(*) as type_count FROM Repairs GROUP BY brigade_number, repair_type")
            type_counts = cursor.fetchall()
            print("\nNumber of each repair type by brigade:")
            for type_count in type_counts:
                print(type_count)

            # Запит 6 (з параметром, який можна змінити)
            depot_name = "Фастів"  # Можна змінити на інше ім'я депо
            cursor.execute("SELECT * FROM Locomotives WHERE depot = %s", (depot_name,))
            depot_locomotives = cursor.fetchall()
            print(f"\nLocomotives assigned to {depot_name} depot:")
            for loco in depot_locomotives:
                print(loco)

    finally:
        connection.close()

if __name__ == "__main__":
    fetch_data_and_structure()
