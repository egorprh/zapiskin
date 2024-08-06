# Замените 'YOUR_API_TOKEN' на ваш токен Telegram бота. Программа создает бота,
# который может отправлять данные каждый день в указанное время.
# Пользователь может установить время рассылки с помощью команды /schedule.
# Время рассылки для каждого пользователя сохраняется в файле 'schedule.json'. Время рассылки проверяется каждую минуту,
# и если текущее время совпадает с установленным временем, отправляются данные из файла 'data.json'.


import asyncio
import datetime
import json

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.storage import MemoryStorage
from aiogram.types import ParseMode

API_TOKEN = 'YOUR_API_TOKEN'
FILENAME = 'schedule.json'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def send_daily_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    for user_id, daily_data in data.items():
        await bot.send_message(user_id, f"Daily Data: {daily_data}", parse_mode=ParseMode.HTML)


async def schedule_daily_task(user_id, schedule_time):
    while True:
        now = datetime.datetime.now()
        target_time = datetime.datetime.strptime(schedule_time, '%H:%M')

        if now.hour == target_time.hour and now.minute == target_time.minute:
            await send_daily_data()

        await asyncio.sleep(60)


@dp.message_handler(commands=['schedule'])
async def set_schedule(message: types.Message):
    try:
        schedule_time = message.text.split(' ')[1]
        user_id = message.from_user.id
    except (IndexError, ValueError):
        return await message.reply("Пожалуйста, укажите время в формате ЧЧ:ММ после команды /schedule.")

    try:
        datetime.datetime.strptime(schedule_time, '%H:%M')
    except ValueError:
        return await message.reply("Неверный формат времени. Пожалуйста, укажите время в формате ЧЧ:ММ.")

    try:
        with open(FILENAME, 'r') as file:
            schedule_data = json.load(file)
    except FileNotFoundError:
        schedule_data = {}

    schedule_data[str(user_id)] = schedule_time

    with open(FILENAME, 'w') as file:
        json.dump(schedule_data, file, indent=4)

    asyncio.create_task(schedule_daily_task(user_id, schedule_time))

    await message.reply(f"Рассылка данных установлена на каждый день в {schedule_time}.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
