import asyncio
from datetime import datetime

from db.pgapi import PGApi


async def test(db):
    print('---Create table---')
    await db.create_table_cities()
    await db.create_table_users()
    print('---Fill table---')
    await db.fill_cities_table()
    print('---SQL query---')
    print(await db.get_records_sql('SELECT * FROM cities WHERE foundation_year = $1', 1703))
    print('---Select all records---')
    print(await db.get_records('cities', {'foundation_year': 1703}))
    print('---Select one record---')
    print(await db.get_record('cities', {'foundation_year': 1703}))
    print('---Is record exist?---')
    print(await db.record_exists('cities', {'foundation_year': 1703}))
    print(await db.record_exists('cities', {'foundation_year': 17233}))
    print('---Get count records---')
    print(await db.count_records('cities', {'foundation_year': 1703}))
    print('---Insert record---')
    userparams = {
        'telegram_id': 132233213,
        'first_name': 'First4',
        'username': 'first4',
    }
    firstuserid = await db.insert_record('users', userparams)
    print(firstuserid)
    print('---Update record---')
    print(await db.update_record('users', firstuserid, {'email': '123@jnfd.ru'}))
    print(await db.get_record('users', {'email': '123@jnfd.ru'}))
    print('---Get field---')
    timecreated: datetime = await db.get_field('users', 'time_created', {'email': '123@jnfd.ru'})
    print(timecreated)
    print(timecreated.timestamp())
    print('---Delete records---')
    print(await db.count_records('cities'))
    # await db.delete_records('cities')
    print(await db.count_records('cities'))
    # await db.delete_records('users')


db = PGApi()
loop = asyncio.get_event_loop()
loop.run_until_complete(db.create())
loop.run_until_complete(test(db))
