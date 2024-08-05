from datetime import datetime
from typing import Union

import asyncpg
from asyncpg import Pool, Connection

import csv

titles = {
    0: "address",
    1: "postal_code",
    2: "country",
    3: "federal_district",
    4: "region_type",
    5: "region",
    6: "area_type",
    7: "area",
    8: "city_type",
    9: "city",
    10: "settlement_type",
    11: "settlement",
    12: "kladr_id",
    13: "fias_id",
    14: "fias_level",
    15: "capital_marker",
    16: "okato",
    17: "oktmo",
    18: "tax_office",
    19: "timezone",
    20: "geo_lat",
    21: "geo_lon",
    22: "population",
    23: "foundation_year"
}


class PGApi:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            host='localhost',
            database='postgres',
            user='apple',
            password='',
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        """
        :param command: скуль запрос
        :param args: аргументы
        :param fetch: выгружаем все строки
        :param fetchval: выгружаем значение
        :param fetchrow: выгружаем одну строку
        :param execute: если не нужен возврат от функции, просто выполнение
        """
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                # print(command)
                # print(*args)
                if fetch:
                    result = await connection.fetch(command, *args)
                    result = [dict(r.items()) for r in result]
                    return result
                elif fetchval:
                    return await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                    return dict(result)
                elif execute:
                    return await connection.execute(command, *args)

    @staticmethod
    def format_args(sql, parameters: dict, glue: str = " AND "):
        # TODO Кажется обработку parameters можно упразднить
        sql += glue.join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, list(parameters.values())

    async def get_record(self, table, params):
        sql = f"SELECT * FROM {table} WHERE "
        sql, params = self.format_args(sql, params)
        return await self.execute(sql, *params, fetchrow=True)

    async def get_field(self, table, field, params):
        sql = f"SELECT {field} FROM {table} WHERE "
        sql, params = self.format_args(sql, params)
        return await self.execute(sql, *params, fetchval=True)

    async def get_records(self, table, params=None):
        if params is None:
            params = {}
        sql = f"SELECT * FROM {table}"
        if params:
            sql += " WHERE "
            sql, params = self.format_args(sql, params)
        return await self.execute(sql, *params, fetch=True)

    async def insert_record(self, table_name: str, params: dict):
        keys = ', '.join(
            f"{item}" for item in params.keys()
        )
        params_mask = ''
        sqlparams = []
        for num, val in enumerate(params.values(), start=1):
            params_mask += f"${num}"
            if num != len(params.values()):
                params_mask += ','
            sqlparams.append(val)
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({params_mask}) RETURNING id;"
        try:
            return await self.execute(sql, *sqlparams, fetchval=True)
        except asyncpg.exceptions.UniqueViolationError:
            return await self.get_field(table_name, 'id', params)

    async def update_record(self, table_name: str, recordid: int, params: dict):
        now = datetime.now()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        params['time_modified'] = datetime.now(local_tz)
        sql = f"UPDATE {table_name} SET "
        sql, sqlparams = self.format_args(sql, params, ", ")
        sql += f" WHERE id = ${len(sqlparams) + 1};"
        sqlparams.append(recordid)
        await self.execute(sql, *sqlparams, execute=True)

    async def get_records_sql(self, sql: str, *args):
        return await self.execute(sql, *args, fetch=True)

    async def delete_records(self, table_name: str):
        await self.execute(f"DELETE FROM {table_name} WHERE TRUE", execute=True)

    async def count_records(self, table: str, params=None):
        if params is None:
            params = {}
        sql = f"SELECT COUNT(id) AS count FROM {table}"
        if params:
            sql += " WHERE "
            sql, params = self.format_args(sql, params)
        return await self.execute(sql, *params, fetchval=True)

    async def record_exists(self, table: str, params):
        sql = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE "
        sql, params = self.format_args(sql, params)
        sql += ')'
        return await self.execute(sql, *params, fetchval=True)

    async def backup_tables(self):
        await self.pool.copy_from_table('words', output='tgbot/db/words.csv', header=True, delimiter=';', format='csv')
        await self.pool.copy_from_table('users', output='tgbot/db/users.csv', header=True, delimiter=';', format='csv')

    async def restore_tables(self):
        await self.pool.copy_to_table('words', source='tgbot/db/words.csv', header=True, delimiter=';', format='csv')
        await self.pool.copy_to_table('users', source='tgbot/db/users.csv', header=True, delimiter=';', format='csv')

    async def create_table_cities(self):
        sql = """CREATE TABLE IF NOT EXISTS cities (
                    id SERIAL PRIMARY KEY,
                    address VARCHAR(255) NOT NULL,
                    city VARCHAR(255),
                    postal_code INTEGER,
                    region VARCHAR(255),
                    district VARCHAR(255),
                    timezone VARCHAR(255),
                    geo_lat REAL,
                    geo_lon REAL,
                    population INTEGER,
                    foundation_year INTEGER
                );"""
        await self.execute(sql, execute=True)

    async def fill_cities_table(self):
        with open('city.csv', newline='') as csvfile:
            cityreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 1
            for row in cityreader:

                # Пропускаем первую строку, там заголовки
                if i == 1:
                    i += 1
                    continue

                await self.insert_record('cities',
                                         # по строке address будем производить поиск поэтому
                                         # приводим её к нижнему регистру для удобства
                                         {'address': row[0].lower(),
                                          'city': row[8] + ' ' + row[9],
                                          'postal_code': int(row[1]) if len(row[1]) > 0 else 0,
                                          'region': row[4] + ' ' + row[5],
                                          'district': row[3],
                                          'timezone': row[19],
                                          'geo_lat': float(row[20]),
                                          'geo_lon': float(row[21]),
                                          'population': int(row[22]),
                                          'foundation_year': int(row[23])}
                                         )

    async def create_table_users(self):
        sql = """CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    username VARCHAR(255) UNIQUE NOT NULL,
                    custom_username VARCHAR(255),
                    language_code VARCHAR(255),
                    email VARCHAR(255),
                    user_timezone VARCHAR(255),
                    referrer_id BIGINT,
                    time_modified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    ); 
                  """
        await self.execute(sql, execute=True)

    # TODO Добавить в таблицы автора и кто последний редачил
    async def create_table_service(self):
        sql = """CREATE TABLE IF NOT EXISTS service(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    time_modified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    ); 
                  """
        await self.execute(sql, execute=True)

    async def create_table_employee(self):
        sql = """CREATE TABLE IF NOT EXISTS employee(
                    id SERIAL PRIMARY KEY,
                    userid INT NOT NULL,
                    description TEXT NOT NULL,
                    role VARCHAR(100) NOT NULL,
                    time_modified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    ); 
                  """
        await self.execute(sql, execute=True)

    async def create_table_service_slot(self):
        sql = """CREATE TABLE IF NOT EXISTS service_slot(
                    id SERIAL PRIMARY KEY,
                    service_id INT NOT NULL,
                    employee_id INT NOT NULL,
                    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
                    duration INT NOT NULL,
                    time_modified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    ); 
                  """
        await self.execute(sql, execute=True)

    async def create_table_appointment(self):
        sql = """CREATE TABLE IF NOT EXISTS appointment(
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL,
                    slot_id INT NOT NULL,
                    time_modified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    ); 
                  """
        await self.execute(sql, execute=True)