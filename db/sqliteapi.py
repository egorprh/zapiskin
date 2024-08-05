import sqlite3


class SqliteDB:
    def __init__(self, path_to_db='tgbot/misc/main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, params: tuple = tuple(), fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        # Задаем чтобы возвращались словари, а не туплы
        connection.row_factory = sqlite3.Row
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
            # Преобразуем объект sqlite3.Row в словарь
            dictone = {}
            if data:
                for key, item in enumerate(cursor.description):
                    dictone[item[0]] = data[key]
            data = dictone
        if fetchall:
            # data = cursor.fetchall()
            # Преобразуем объекты sqlite3.Row в словари
            # TODO Можем тут упасть, если cursor.fetchall() будет None
            data = [dict(row) for row in cursor.fetchall()]

        connection.close()

        return data

    @staticmethod
    def format_args(sql, params: dict, separator: str = " AND "):
        sql += separator.join(
            f"{item} = ?" for item in params.keys()
        )
        return sql, tuple(params.values())

    def get_record(self, table, **kwargs):
        sql = f"SELECT * FROM {table} WHERE "
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, params, fetchone=True)

    def get_records(self, table, params=None):
        if params is None:
            params = {}
        sql = f"SELECT * FROM {table}"
        if params:
            sql += " WHERE "
            sql, params = self.format_args(sql, params)
        return self.execute(sql, params, fetchall=True)

    def insert_record(self, table_name: str, **kwargs):
        keys = ', '.join(
            f"{item}" for item in kwargs.keys()
        )
        params_mask = ', '.join(
            '?' for item in kwargs.keys()
        )
        params = tuple(kwargs.values())
        sql = f"INSERT OR IGNORE INTO {table_name} ({keys}) VALUES ({params_mask})"
        self.execute(sql, params, commit=True)

    def update_record(self, table_name: str, recordid: int, **kwargs):
        sql = f"UPDATE {table_name} SET "
        sql, params = self.format_args(sql, kwargs, ", ")
        sql += " WHERE id = ?"
        params += (recordid,)
        self.execute(sql, params, commit=True)

    def get_records_sql(self, sql: str, *args):
        return self.execute(sql, args, fetchall=True)

    def delete_records(self, table_name: str):
        self.execute(f"DELETE FROM {table_name} WHERE TRUE", commit=True)

    def count_records(self, table: str, params=None):
        if params is None:
            params = {}
        sql = f"SELECT COUNT(id) AS count FROM {table}"
        if params:
            sql += " WHERE "
            sql, params = self.format_args(sql, params)
        return self.execute(sql, params, fetchone=True).get('count')


def logger(statement):
    print(f'''
    ------------------------------------------
    Executing:
    {statement}
    ------------------------------------------
    ''')
