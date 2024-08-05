from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.pgapi import PGApi

from datetime import datetime, timezone


# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


class ServiceData(StatesGroup):
    name = State()
    description = State()
    price = State()


@router.message(StateFilter(None), Command("addservice"))
async def set_service(message: Message, state: FSMContext):
    await state.set_state(ServiceData.name)
    await message.answer("Введите название услуги")


@router.message(ServiceData.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ServiceData.description)
    await message.reply("Введите описание услуги")


@router.message(ServiceData.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ServiceData.price)
    await message.reply("Введите стоимость услуги")


@router.message(ServiceData.price)
async def process_price(message: Message, state: FSMContext, db: PGApi):
    try:
        price = float(message.text)
    except ValueError:
        return await message.reply("Пожалуйста, введите числовое значение для стоимости услуги.")

    await state.update_data(price=price)

    data = await state.get_data()
    await db.insert_record('service', {'name': data.get('name'),
                                             'price': data.get('price'),
                                             'description': data.get('description')})
    await state.clear()

    await message.reply("Услуга успешно добавлена")