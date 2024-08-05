# импорты
from config_reader import config
import asyncio
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram import html
from aiogram.utils.formatting import Text, Bold

from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

from aiogram.client.default import DefaultBotProperties

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        # parse_mode=ParseMode.HTML
        # тут ещё много других интересных настроек
    )
)

# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
# bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /test1
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


# Хэндлер на команду /test2
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")

# Если не указать фильтр F.text,
# то хэндлер сработает даже на картинку с подписью /test
@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    await message.answer(
        "Hello, <b>world</b>!",
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\!",
        parse_mode=ParseMode.MARKDOWN_V2
    )

    # где-то в функции...
    await message.answer("Сообщение с <u>HTML-разметкой</u>")
    # чтобы явно отключить форматирование в конкретном запросе,
    # передайте parse_mode=None
    await message.answer(
        "Сообщение без <s>какой-либо разметки</s>",
        parse_mode=None
    )


@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")

# Экранирование <Cлавик777>
@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML
    )


# Экранирование <Cлавик777> продвинутый способ
@dp.message(Command("hello2"))
async def cmd_hello(message: Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )


@dp.message(Command("settimer"))
async def cmd_settimer(
        message: Message,
        command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer <time> <message>"
        )
        return
    await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {text_to_send}"
    )


@dp.message(Command("custom1", prefix="%"))
async def cmd_custom1(message: Message):
    await message.answer("Вижу команду!")

@dp.message(Command("help"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "help"
))
async def cmd_start_help(message: Message):
    await message.answer("Это сообщение со справкой")


@dp.message(CommandStart(
    deep_link=True,
    magic=F.args.regexp(re.compile(r'book_(\d+)'))
))
async def cmd_start_book(
        message: Message,
        command: CommandObject
):
    book_number = command.args.split("_")[1]
    await message.answer(f"Sending book №{book_number}")


@dp.message(Command("links"))
async def cmd_links(message: Message):
    links_text = (
        "https://nplus1.ru/news/2024/05/23/voyager-1-science-data"
        "\n"
        "https://t.me/telegram"
    )
    # Ссылка отключена
    options_1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(
        f"Нет превью ссылок\n{links_text}",
        link_preview_options=options_1
    )

    # -------------------- #

    # Маленькое превью
    # Для использования prefer_small_media обязательно указывать ещё и url
    options_2 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True
    )
    await message.answer(
        f"Маленькое превью\n{links_text}",
        link_preview_options=options_2
    )

    # -------------------- #

    # Большое превью
    # Для использования prefer_large_media обязательно указывать ещё и url
    options_3 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_large_media=True
    )
    await message.answer(
        f"Большое превью\n{links_text}",
        link_preview_options=options_3
    )

    # -------------------- #

    # Можно сочетать: маленькое превью и расположение над текстом
    options_4 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True,
        show_above_text=True
    )
    await message.answer(
        f"Маленькое превью над текстом\n{links_text}",
        link_preview_options=options_4
    )

    # -------------------- #

    # Можно выбрать, какая ссылка будет использоваться для предпосмотра,
    options_5 = LinkPreviewOptions(
        url="https://t.me/telegram"
    )
    await message.answer(
        f"Предпросмотр не первой ссылки\n{links_text}",
        link_preview_options=options_5
    )


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(F.text)
async def echo_with_time(message: Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="HTML")



# Запуск процесса поллинга новых апдейтов
async def main():
    # Где-то в другом месте, например, в функции main():
    dp.message.register(cmd_test2, Command("test2"))
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
