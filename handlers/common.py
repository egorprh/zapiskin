import json

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from db.pgapi import PGApi

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext, db: PGApi):
    user = message.from_user

    if await db.record_exists('users', {'telegram_id': user.id}):
        await message.answer('Ты уже нажимал старт')
    else:
        db_userid = await db.insert_record('users', {'telegram_id': user.id,
                                                     'first_name': user.first_name,
                                                     'username': user.username,
                                                     'language_code': user.language_code})
    await state.clear()
    await message.answer(
        text="Добро пожаловать! Я помогаю записываться на услуги.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["getmyappointments"]))
async def cmd_cancel(message: Message, state: FSMContext, db: PGApi):
    #TODO Вынести в отдельную функцию и переиспользовать
    sql = 'SELECT a.id AS aid, ss.* FROM service_slot ss ' \
          'LEFT JOIN appointment a ON ss.id = a.slot_id ' \
          'WHERE a.user_id = $1 '
    slots = await db.get_records_sql(sql, message.from_user.id)
    text = ''
    if len(slots) == 0:
        text = 'Нет активных записей'

    for slot in slots:
        service_name = await db.get_field('service', 'name', {'id': slot['service_id']})
        text += f"{slot['aid']}. Услуга: {service_name}, Сотрудник: {slot['employee_id']}, Время: {slot['start_time'].strftime('%Y-%m-%d %H:%M')}\n"

    await message.answer(text)


@router.message(Command(commands=['commands']))
async def get_commands(message: Message, db: PGApi):
    await message.reply(
        '/addemployee \n'
        '/addservice \n'
        '/addschedule \n'
        '/appointment \n'
        '/getmyappointments \n'
        '/cancel \n'
        '/cancelmyapp \n'
    )

#TODO Заглушку базовую реализовать
