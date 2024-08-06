import json

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()
FILENAME = 'user_data.json'


# TODO Валидация введенных данных

# состояния
class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    email = State()
    age = State()
    gender = State()
    city = State()


# обработчик команды /start
@router.message(StateFilter(None), Command("register"))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(Form.name)


# обработчик для фамилии
@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await state.set_state(Form.surname)
    await message.answer("Какая у тебя фамилия?")


# повторяем для каждого поля
@router.message(Form.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.lower())
    await state.set_state(Form.phone)
    await message.answer("Какой у тебя номер телефона?")


@router.message(Form.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.lower())
    await state.set_state(Form.email)
    await message.answer("Какой у тебя email?")


@router.message(Form.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text.lower())
    await state.set_state(Form.gender)
    await message.answer("Какой у тебя пол?")


@router.message(Form.gender)
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text.lower())
    await state.set_state(Form.city)
    await message.answer("В каком городе ты живешь?")


@router.message(Form.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.lower())
    user_data = await state.get_data()
    user_id = message.from_user.id

    schedule_data = {str(user_id): user_data.items()}

    with open(FILENAME, 'w') as file:
        json.dump(schedule_data, file, indent=4)

    # # сохраняем данные в файл
    # with open('user_data.txt', 'a') as file:
    #     for key, value in user_data.items():
    #         file.write(f'{key}: {value}\n')

    await state.clear()
    await message.answer("Спасибо! Данные сохранены.")
