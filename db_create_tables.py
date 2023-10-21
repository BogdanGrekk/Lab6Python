import pymysql

def create_tables():
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
            # Створення таблиці Локомотиви
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Locomotives (
                    locomotive_id INT PRIMARY KEY AUTO_INCREMENT,
                    registration_number VARCHAR(255) NOT NULL,
                    depot VARCHAR(255) NOT NULL,
                    locomotive_type ENUM('cargo', 'passenger') NOT NULL,
                    year_of_production YEAR NOT NULL
                )
            ''')

            # Створення таблиці Ремонти
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Repairs (
                    repair_id INT PRIMARY KEY AUTO_INCREMENT,
                    locomotive_id INT,
                    repair_type ENUM('current', 'maintenance', 'unscheduled') NOT NULL,
                    start_date DATE NOT NULL,
                    days_required INT NOT NULL,
                    daily_repair_cost DECIMAL(10, 2) NOT NULL,
                    brigade_number INT,
                    FOREIGN KEY (locomotive_id) REFERENCES Locomotives(locomotive_id)
                )
            ''')

            # Створення таблиці Бригади
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Brigades (
                    brigade_number INT PRIMARY KEY,
                    phone VARCHAR(15) NOT NULL
                )
            ''')

            # Створення таблиці Робітники
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Workers (
                    worker_id INT PRIMARY KEY AUTO_INCREMENT,
                    last_name VARCHAR(255) NOT NULL,
                    first_name VARCHAR(255) NOT NULL,
                    middle_name VARCHAR(255),
                    brigade_number INT,
                    is_brigade_leader BOOLEAN NOT NULL,
                    birth_date DATE NOT NULL,
                    FOREIGN KEY (brigade_number) REFERENCES Brigades(brigade_number)
                )
            ''')

        # Зберігаємо зміни
        connection.commit()

    finally:
        connection.close()

if __name__ == "__main__":
    create_tables()
