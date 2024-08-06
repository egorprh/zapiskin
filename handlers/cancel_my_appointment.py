from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.pgapi import PGApi

from datetime import datetime, timezone

# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


class CancelData(StatesGroup):
    appointments = State()


@router.message(StateFilter(None), Command("cancelmyapp"))
async def get_appointments(message: Message, state: FSMContext, db: PGApi):
    await state.set_state(CancelData.appointments)
    # TODO Вынести в отдельную функцию и переиспользовать
    sql = 'SELECT a.id AS aid, ss.* FROM service_slot ss ' \
          'LEFT JOIN appointment a ON ss.id = a.slot_id ' \
          'WHERE a.user_id = $1 '
    slots = await db.get_records_sql(sql, message.from_user.id)
    text = ''
    if len(slots) == 0:
        text = 'Нет активных записей'
        await state.clear()

    for slot in slots:
        # TODO ввести LIMIT в pg api
        service_name = await db.get_field('service', 'name', {'id': slot['service_id']})
        text += f"{slot['aid']}. Услуга: {service_name}, Сотрудник: {slot['employee_id']}, Время: {slot['start_time'].strftime('%Y-%m-%d %H:%M')}\n"

    await message.answer(text)
    await message.answer("Введите номер слота, который хотите отменить.")


@router.message(CancelData.appointments)
async def cancel_appointment(message: Message, state: FSMContext, db: PGApi):
    try:
        app_id = float(message.text)
    except ValueError:
        return await message.reply("Пожалуйста, введите числовое значение")

    #TODO Проверка, что это точно моя запись! Не чужая. Для админа наверное будет админка
    # + Проврка на то, если такая запись
    await db.delete_record('appointment', {'id': app_id})
    await state.clear()
    await message.reply("Запись успешно отменена!")
