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
        text="Добро пожаловать! Я помогаю не забывать оплачивать подписки. "
             "С помощью команды  /addsub ты можешь добавить подписку."
             "За день до наступления даты оплаты, в 12:00, я тебе напомню о ней."
             "С помощью команды /getmysubs ты можешь посмотреть свои добавленные подписки.",

        reply_markup=ReplyKeyboardRemove()
    )


# Нетрудно догадаться, что следующие два хэндлера можно
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=['commands']))
async def get_commands(message: Message, db: PGApi):
    await message.reply(
        '/addemployee'
        '/addservice'
        '/addschedule'
        '/appointment'
    )

