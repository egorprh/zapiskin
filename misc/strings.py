import asyncio
from random import randint

from aiogram import types
from aiogram.types import ChatActions
from aiogram.utils import emoji
from aiogram.utils.markdown import text


async def typing(message: types.Message):
    await message.bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await asyncio.sleep(randint(4, 10) / 10)


async def record_voice(message: types.Message):
    await message.bot.send_chat_action(message.from_user.id, ChatActions.RECORD_VOICE)
    await asyncio.sleep(randint(4, 10) / 10)


lang_strings: dict = {}

# Plug handler
lang_strings['plug'] = emoji.emojize('Внизу есть кнопки и меню, пользуйся ими, пожалуйста :point_down:')
lang_strings['what_do'] = emoji.emojize(':8ball: Чем займемся на этот раз?)')

# Acquaintance handler messages
lang_strings['hello'] = text(emoji.emojize('''
Привет! Давай знакомиться)

Меня зовут Лэнг Уик. Как Джон Уик, только Лэнг Уик. :sweat_smile:
Можно просто Ленгвик.)

Меня создали, чтобы я помогал изучать тебе иностранные языки.
Как я могу обращаться к тебе?'''))
lang_strings['acquaintance'] = text(emoji.emojize(":clap: Рад знакомству, username!"))
lang_strings['about'] = text("Рассказать тебе подробнее про то, что я умею?")
lang_strings['first_function'] = text(emoji.emojize('''
:one: Первая моя функция - это личный словарь. 
Ты можешь отправлять мне новые слова, 
которые хочешь изучить, что бы я тебя потом по ним тренировал.

Это очень удобно, я в любой момент буду готов записать слово в твой личный словарь.

Для сохранения слова:
1) Нажми кнопку "Записать слово"
2) Запиши слово и словосочетание на иностранном языке
3) Запиши перевод слова и словосочетания. Я специально не буду помогать тебе с переводом, 
потому что так ты лучше запомнишь написание слова.
4) Запиши голосовое сообщение с произношением слова и словосочетания. 
Это улучшает запоминание слова и заодно тренирует правильное произношение.'''))
lang_strings['second_function'] = text(emoji.emojize('''
:two: Вторая моя функция - это адаптивный режим тренировки слов.

Я выбирая слова из твоего словарика и даю тебе.
Ты их переводишь и затем оцениваешь слово по предложенной шкале.

Адаптивность заключается в том, что я, на основе твоих оценок, 
определяю как часто тебе выдавать то или иное слово.

Если ты хорошо запоминаешь слово, то оно будет попадаться в тренировках реже, 
интервал между повторениями вырастет.

Если ты слово знаешь плохо или вовсе забыл его, то интервалы повторения слова будут уменьшаться 
и оно будет попадаться тебе чаще, что бы ты смог его выучить получше.

В основе тренировки лежит принцип запоминания Эббингауза.
Герман Эббингауз - это немецкий ученый 19 века, который изучал возможности памяти.
В основе принципа лежит повторение слов, через определенные "правильные" интервалы.
Если коротко, то что бы навсегда запомнить слово (или любую другую информацию) - 
его надо повторять через увеличивающиеся промежутки времени.

Создатель заложил в меня математическую модель на основе данного принципа.
И по этой модели я буду рассчитывать лично для тебя оптимальные промежутки времени, учитывая твой прогресс.
Индивидуальный подход, так сказать!)

Для начала тренировки нажми соответствующую кнопку.

Тренировка проходит следующим образом:
1) Я выдаю тебе слово на английском
2) Ты должен его перевести и можешь даже произнести
3) Я присылаю тебе ответ
4) В зависимости от того, как быстро/правильно ты его вспомнил, тебе надо выставить оценку

Новые слова попадают в тренировку не раньше, чем через час.'''))
lang_strings['you_interesting_too'] = text(emoji.emojize(":relieved: Спасибо!) Я думаю ты тоже)"))
lang_strings['end_of_function'] = text(
    emoji.emojize("На данный момент это все мои функции, но создатель меня обещал научить куче "
                  "всяких фишек."))
lang_strings['sometimes_send_articles'] = text(
    emoji.emojize("Иногда я буду присылать тебе интересные статейки на тему изучения "
                  "иностранных языков."))
lang_strings['at_your_service'] = text(emoji.emojize("Ну а теперь - я к твоим услугам!) :arrow_down:"))

# Acquaintance handler buttons
lang_strings['sure'] = text(emoji.emojize(":relieved: Будьте так добры, мистер Уик!"))
lang_strings['what_else'] = text(emoji.emojize(":ok_hand: Такс, а что еще?"))
lang_strings['interesting_person'] = text(emoji.emojize(":smirk: А ты интересная личность, Ленгвик!"))

# Кнопки рейтинга слова
lang_strings['0_rate'] = emoji.emojize(':skull: {text}')
lang_strings['1_rate'] = emoji.emojize(':sweat_smile: {text}')
lang_strings['2_rate'] = emoji.emojize(':relieved: {text}')
lang_strings['3_rate'] = emoji.emojize(':sunglasses: {text}')
lang_strings['thirty_mins'] = emoji.emojize(':skull: 30 мин')
lang_strings['four_days'] = emoji.emojize(':sweat_smile: 4 дня')
lang_strings['seven_days'] = emoji.emojize(':relieved: 7 дней')
lang_strings['thirteen_days'] = emoji.emojize(':sunglasses: 13 дней')

# Bot functions
lang_strings['get_word'] = emoji.emojize(':pencil2: Записать слово')
lang_strings['start_training'] = emoji.emojize(':bicyclist: Тренировка!')

# Other
lang_strings['second_start'] = emoji.emojize(":cop: Ты уже нажимал на Start, хитрец")
lang_strings['yes'] = emoji.emojize(':white_check_mark: Да')
lang_strings['no'] = emoji.emojize(':negative_squared_cross_mark: Нет')
lang_strings['report_error'] = emoji.emojize(':white_check_mark: Сообщить об ошибке')
lang_strings['error_occurred'] = emoji.emojize(":pencil2: Произошла ошибка при сохранении слова. Попробовать еще раз?")

# Get word handler messages
lang_strings['enter_new_word'] = emoji.emojize(":capital_abcd: Введи новое слово на иностранном языке "
                                               "и любое предложение в котором оно может использоваться")
lang_strings['get_translate'] = emoji.emojize(
    ":arrows_counterclockwise: Теперь введи перевод введенных слова и предложения")
lang_strings['get_audio'] = emoji.emojize(
    ":microphone: Запиши произношение слова и предложения голосом. Если не можешь сейчас записать голосовое сообщение - нажми кнопку")
lang_strings['without_audio'] = emoji.emojize(":mute: Без произношения")
lang_strings['word_saved'] = emoji.emojize("Всё, слово записал себе :white_check_mark:")

# Training handler messages
lang_strings['take_random_words'] = emoji.emojize(
    ":game_die: Для тренировок слов нет, так что дам тебе 5 случайных новых слов")
lang_strings['ok_lets_go'] = emoji.emojize(":vertical_traffic_light: 3... 2... 1... Okaaay, let's GO!")
lang_strings['rate_saved'] = emoji.emojize(":white_check_mark: Оценку зафиксировал")
lang_strings['word:'] = emoji.emojize(':abc: Слово: ')
lang_strings['how_translate:'] = emoji.emojize(':abc: Как переводится: ')
lang_strings['translate:'] = emoji.emojize(':point_right: Перевод: ')
lang_strings['pronounce:'] = emoji.emojize(':sound: Произношение: ')
lang_strings['no_voice'] = emoji.emojize('А произношение ты не записал. Не забудь в следующий раз. :point_up:')
lang_strings['training_is_over'] = emoji.emojize(
    ":thumbsup: Фух! Тренировка окончена! Количество правильных ответов: {var}. Дай пять!")
lang_strings['rate_not_saved'] = emoji.emojize(":pensive: Не удалось сохранить оценку, обратитесь в поддержку")
lang_strings['burst_emoji'] = emoji.emojize(":boom:")
lang_strings['show_word'] = emoji.emojize(":cloud: Не помню, покажи слово")
lang_strings['totally_right'] = emoji.emojize("Совершенно верно :thumbsup:")
lang_strings['some_wrong'] = emoji.emojize("Немножечко ошибся :grin:")
lang_strings['when_repeat_word'] = emoji.emojize("Через сколько повторим слово? :watch:")
lang_strings['no_voice_for_base_word'] = emoji.emojize(":mute: У слов из общей базы пока нет записанного произношения")
lang_strings['no_word_for_training'] = emoji.emojize(":coffee: Слов для тренировки пока нет")

# Training handler buttons
lang_strings['give_five_emoji'] = emoji.emojize(":raised_hand:")
lang_strings['next_word'] = emoji.emojize(":arrow_right: Следующее слово")
lang_strings['stop_training'] = emoji.emojize(":x: Закончить тренировку")
lang_strings['press_button'] = emoji.emojize(":arrow_down: Нажми кнопку")
