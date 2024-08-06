import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# настройка логгирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
API_TOKEN = 'YOUR_API_TOKEN'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await Form.name.set()
    await message.answer("Привет! Как тебя зовут?")


# обработчик для каждого вопроса
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.answer("Какая у тебя фамилия?")


# повторяем для каждого поля
@dp.message_handler(state=Form.surname)
async def process_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await Form.next()
    await message.answer("Какой у тебя номер телефона?")


@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await Form.next()
    await message.answer("Какой у тебя email?")


@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await Form.next()
    await message.answer("Сколько тебе лет?")


@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await Form.next()
    await message.answer("Какой у тебя пол?")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await Form.next()
    await message.answer("В каком городе ты живешь?")


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    # сохраняем данные в файл
    with open('user_data.txt', 'a') as file:
        for key, value in data.items():
            file.write(f'{key}: {value}\n')

    await state.finish()
    await message.answer("Спасибо! Данные сохранены.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.skip_updates())
    loop.run_until_complete(dp.start_polling())
