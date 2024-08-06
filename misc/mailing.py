from datetime import datetime

from aiogram import Bot

from db.pgapi import PGApi


async def mailing(bot: Bot, db: PGApi):
    records = await db.get_records('subscriptions')

    now = datetime.now().timestamp()

    for record in records:
        if record['paydate'].timestamp() - (3600 * 24) > now:
            await bot.send_message(record['userid'],
                                   f"Завтра наступит дата оплаты подписки {record['name']}. "
                                   f"Сумма к оплате {record['price']}")
