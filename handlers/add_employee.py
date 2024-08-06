from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from db.pgapi import PGApi

# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


class EmployeeData(StatesGroup):
    userid = State()
    description = State()


@router.message(StateFilter(None), Command("addemployee"))
async def set_employee(message: Message, state: FSMContext):
    await state.set_state(EmployeeData.userid)
    await message.answer("Введите идентификатор пользователя в телеграм")


@router.message(EmployeeData.userid)
async def process_userid(message: Message, state: FSMContext):
    try:
        userid = float(message.text)
    except ValueError:
        return await message.reply("Пожалуйста, введите числовое значение для стоимости услуги.")

    await state.update_data(userid=userid)
    await state.set_state(EmployeeData.description)
    await message.reply("Введите описание для сотрудника")


@router.message(EmployeeData.description)
async def process_description(message: Message, state: FSMContext, db: PGApi):
    await state.update_data(description=message.text)

    data = await state.get_data()

    await db.insert_record('employee', {'userid': data.get('userid'),
                                        'description': data.get('description'),
                                        'role': 'employee'})
    await state.clear()

    await message.reply("Сотрудник успешно добавлен")
