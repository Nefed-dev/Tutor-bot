import sqlite3

class Database:
    """Класс, отвечающий за базу данных"""
    def __init__(self, path_to_db):
        path_to_db = path_to_db

    def connection(self):
        """Подключение базы данных"""
        pass
    def excecute(self):

        pass
    def create_table(self):
        """Создание таблицы: id, fullname(tg), phone_number"""
        """В дальнейшем необходимо добавить в таблицу желание записаться на курс/интенсив"""
        pass
    def format_args(self):
        """Форматирование аргументов, для удобного составления запроса в бд"""
        pass
    def add_user(self):
        """Добавление пользователя в БД"""
        pass
    def select_user(self):
        """Выбор пользователя из БД"""
        pass
    def select_all_user(self):
        """Выбор всех пользователей"""
        pass
    def update_user_phone_number(self):
        """Добавление номера телефона в БД"""
        pass
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
