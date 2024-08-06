import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from db.pgapi import PGApi
from handlers import common, add_service, add_employee, add_schedule, appointment, cmd_cancel, \
    cancel_my_appointment

# https://t.me/podpiskin007_bot

logger = logging.getLogger(__name__)


async def create_tables(db: PGApi):
    logger.info("Create DB connection")
    await db.create()
    logger.info("Create tables if not exist")
    await db.create_table_users()
    await db.create_table_service()
    await db.create_table_employee()
    await db.create_table_service_slot()
    await db.create_table_appointment()
    logger.info("DB ready")


# Запуск бота
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # Но явное лучше неявного =]
    dp = Dispatcher(storage=MemoryStorage())
    dp['db'] = db = PGApi()

    bot = Bot(token=config.bot_token.get_secret_value())

    dp.include_routers(
        cmd_cancel.router,
        add_service.router,
        add_employee.router,
        add_schedule.router,
        appointment.router,
        cancel_my_appointment.router,
        common.router
    )

    # Инициализируем рассылку
    # TODO Передать скедулер в мидлварь
    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(mailing.mailing, trigger='cron',
    #                   hour='12', minute='01', start_date=datetime.now(), kwargs={'bot': bot, 'db': db})
    # scheduler.start()

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await create_tables(db)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
