from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from db.pgapi import PGApi

# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


class AppointmentData(StatesGroup):
    slots = State()


@router.message(StateFilter(None), Command("appointment"))
async def get_appointments(message: Message, state: FSMContext, db: PGApi):
    await state.set_state(AppointmentData.slots)
    await state.update_data(userid=message.from_user.id)
    await message.answer("Выберите слот и введите его номер")
    sql = 'SELECT ss.* FROM service_slot ss ' \
          'LEFT JOIN appointment a ON ss.id = a.slot_id AND a.user_id = $1 ' \
          'WHERE a.id IS NULL ' \
          'LIMIT 10'
    slots = await db.get_records_sql(sql, message.from_user.id)
    text = ''
    if len(slots) == 0:
        text = 'Нет доступных слотов для записи'

    for slot in slots:
        # TODO ввести LIMIT в pg api
        service_name = await db.get_field('service', 'name', {'id': slot['service_id']})
        text += f"{slot['id']}. Услуга: {service_name}, Сотрудник: {slot['employee_id']}, Время: {slot['start_time'].strftime('%Y-%m-%d %H:%M')}\n"

    await message.answer(text)


@router.message(AppointmentData.slots)
async def appointment(message: Message, state: FSMContext, db: PGApi):
    try:
        slotid = float(message.text)
    except ValueError:
        return await message.reply("Пожалуйста, введите числовое значение для стоимости услуги.")

    data = await state.get_data()

    # TODO получать userid из users?
    await db.insert_record('appointment', {'slot_id': slotid,
                                           'user_id': data.get('userid')})
    await state.clear()

    await message.reply("Вы успешно записаны!")
