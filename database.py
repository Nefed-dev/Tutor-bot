import sqlite3

class Database:
    def __init__(self, path_to_db='users.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str,
                parameters: tuple = None, 
                fetchone=False,
                fetchall=False,
                commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = self.connection()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            connection.fetchall()
        if fetchone:
            connection.fetchone()
        return data

    def create_table_users(self):
        sql = """
            CREATE TABLE Users (
                id int NOT NULL,
                Name varchar(255) NOT NULL,
                phone int NOT NULL,
                PRIMARY KEY (id)
                );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f'{item} = ?' for item in parameters])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, phone: int):
        sql = """
        INSERT INTO Users(id, Name, phone) VALUES (?, ?, ?)"""
        self.execute(sql, parameters=(id, name, phone), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):

        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
