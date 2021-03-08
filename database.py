import sqlite3

class Database:
    def __init__(self, path_to_db):
        path_to_db = path_to_db

    def connection(self):
        pass
    def excecute(self):
        pass
    def create_table(self):
        pass
    def format_args(self):
        pass
    def add_user(self):
        pass
    def select_user(self):
        pass
    def select_all_user(self):
        pass
    def update_user_phone_number(self):
        pass
    def delete_user(self):
        pass

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
