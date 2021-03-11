import sqlite3


class Database:
    """Класс, отвечающий за базу данных"""

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    def connection(self):
        """Подключение базы данных"""
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):

        if not parameters:
            parameters = ()

        connection = self.connection()
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()

        connection.close()
        return data

    def create_table(self):
        """Создание таблицы: id, fullname(tg), phone_number"""
        """В дальнейшем необходимо добавить в таблицу желание записаться на курс/интенсив"""
        sql = """
        CREATE TABLE Users (
        id int NOT NULL,
        fullname varchar(255) NOT NULL, 
        phone varchar(12),
        PRIMARY KEY (id)
        )"""

        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        """Форматирование аргументов, для удобного составления запроса в БД"""
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])

        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, phone: str = None):
        """Добавление пользователя в БД"""
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        sql = """
        INSERT INTO Users(id, fullname, phone) VALUES (?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, phone), commit=True)

    def select_all_users(self):
        """Выбор всех пользователей"""
        sql = """SELECT * FROM Users"""
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        """Выбор пользователя из БД"""
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_phone(self, phone, id):
        """Добавление номера телефона в БД"""
        # SQL_EXAMPLE = "UPDATE Users SET phone=+79876543210 WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone=? WHERE id=?
        """

        return self.execute(sql, parameters=(phone, id), commit=True)

    def check_phone(self, id):
        sql = f"""
        SELECT phone FROM Users WHERE id=?
        """

        return self.execute(sql, parameters=id, fetchone=True)

    def delete_user(self):
        """Удаление пользователя из БД"""
        pass


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
