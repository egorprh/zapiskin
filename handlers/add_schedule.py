from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from db.pgapi import PGApi

from datetime import datetime, timedelta

import pytz

# TODO Валидация на количество введенных символом и ввведно сообщения, обработка эксепшенов


router = Router()


@router.message(StateFilter(None), Command("addschedule"))
async def set_schedule(message: Message, db: PGApi):
    slots = create_schedule()
    services = await db.get_records('service')
    employees = await db.get_records('employee')
    for service in services:
        for employee in employees:
            for slot in slots:
                await db.insert_record('service_slot', {'service_id': service['id'],
                                                        'employee_id': employee['id'],
                                                        'start_time': slot,
                                                        'duration': 3600,
                                                        })
    await message.answer("Расписание создано")


def create_schedule():
    schedule = []
    today = datetime.now(pytz.utc)

    # Начало и конец рабочего дня
    start_time = today.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=21, minute=0, second=0, microsecond=0)

    # Создаём расписание на ближайшую неделю
    for day in range(7):
        current_day = today + timedelta(days=day)
        # Обновляем время начала и конца для текущего дня
        current_start_time = start_time.replace(year=current_day.year, month=current_day.month, day=current_day.day)
        current_end_time = end_time.replace(year=current_day.year, month=current_day.month, day=current_day.day)

        current_time = current_start_time

        while current_time < current_end_time:
            schedule.append(current_time)
            current_time += timedelta(hours=1)  # Добавляем 1 час

    return schedule
