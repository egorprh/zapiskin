from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.pgapi import PGApi

from datetime import datetime, timezone


# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


class SubscriptionData(StatesGroup):
    name = State()
    price = State()
    paydate = State()
    link = State()


@router.message(StateFilter(None), Command("addsub"))
async def set_subscription(message: Message, state: FSMContext):
    await state.set_state(SubscriptionData.name)
    await message.answer("Введите название подписки")


@router.message(SubscriptionData.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SubscriptionData.price)
    await message.reply("Введите стоимость подписки:")


@router.message(SubscriptionData.price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        return await message.reply("Пожалуйста, введите числовое значение для стоимости подписки.")

    await state.update_data(price=price)
    await state.set_state(SubscriptionData.paydate)
    await message.reply("Введите дату платежа (в формате ДД.ММ.ГГГГ):")


@router.message(SubscriptionData.paydate)
async def process_paydate(message: Message, state: FSMContext, db: PGApi):
    try:
        date_obj = datetime.strptime(message.text, "%d.%m.%Y")
        timestamp = datetime.fromtimestamp(date_obj.timestamp(), timezone.utc)
        await state.update_data(paydate=timestamp)

        user = message.from_user
        user_data = await state.get_data()
        # TODO брать ид юзера из таблицы users а в эту записывать ид из таблицы юзерс
        await db.insert_record('subscriptions', {'userid': user.id,
                                                 'name': user_data.get('name'),
                                                 'price': user_data.get('price'),
                                                 'paydate': user_data.get('paydate')})
        await state.clear()

        await message.reply("Подписка успешно сохранена!")
    except ValueError:
        await message.reply("Неверный формат даты! Введи еще раз")


# @router.message(SubscriptionData.paydate)
# async def process_paydate(message: Message, state: FSMContext):
#     try:
#         date_obj = datetime.strptime(message.text, "%d.%m.%Y")
#         timestamp = datetime.fromtimestamp(date_obj.timestamp(), timezone.utc)
#         await state.update_data(paydate=timestamp)
#         await state.set_state(SubscriptionData.link)
#         await message.reply("Введите ссылку на сервис:")
#     except ValueError:
#         await message.reply("Неверный формат даты! Введи еще раз")
#
# @router.message(SubscriptionData.link)
# async def process_link(message: Message, state: FSMContext, db: PGApi):
#     await state.update_data(link=message.text)
#
#     user = message.from_user
#     user_data = await state.get_data()
#
#     #TODO брать ид юзера из таблицы users а в эту записывать ид из таблицы юзерс
#     await db.insert_record('subscriptions', {'userid': user.id,
#                                              'name': user_data.get('name'),
#                                              'link': user_data.get('link'),
#                                              'price': user_data.get('price'),
#                                              'paydate': user_data.get('paydate')})
#     await state.clear()
#
#     await message.reply("Подписка успешно сохранена!")
