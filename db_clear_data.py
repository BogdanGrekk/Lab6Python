import pymysql

def clear_data():
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
            # Видалення даних з таблиць
            cursor.execute('DELETE FROM Repairs')
            cursor.execute('DELETE FROM Workers')
            cursor.execute('DELETE FROM Brigades')
            cursor.execute('DELETE FROM Locomotives')

        # Зберігаємо зміни
        connection.commit()

    finally:
        connection.close()

if __name__ == "__main__":
    clear_data()
