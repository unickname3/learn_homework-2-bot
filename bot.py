import logging
from datetime import date
import locale

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
from dateutil.parser import parse

import settings
from cities_game import CitiesSession

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)

locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))


def greet_user(update, context):
    text = "Вызван /start"
    update.message.reply_text(text)


def talk_to_me(update, context):
    """
    Echo
    """
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def planet_where(update, context):
    """
    In which constellation users planet today?
    """
    user_text = update.message.text
    try:
        planet = user_text.split()[1].capitalize()
    except IndexError:
        reply = "Введите название планеты"
        update.message.reply_text(reply)
        return

    planet_constructors = {
        "Mercury": ephem.Mercury,
        "Venus": ephem.Venus,
        "Mars": ephem.Mars,
        "Jupiter": ephem.Jupiter,
        "Saturn": ephem.Saturn,
        "Uranus": ephem.Uranus,
        "Neptune": ephem.Neptune,
    }

    planet_constructor = planet_constructors.get(planet, None)

    if planet_constructor:
        planet_obj = planet_constructor()
        planet_obj.compute(date.today())
        planets_constellation = ephem.constellation(planet_obj)
        reply = f"{planet} в созвездии {planets_constellation[1]}"
    else:
        reply = "Не знаю планеты такой."

    update.message.reply_text(reply)


def wordcount(update, context):
    """
    Count number of word in users message
    """
    user_text = update.message.text.strip()

    words = user_text.split()

    if len(words) == 1:
        reply = "Не обнаружено текста для подсчёта слов!"
        update.message.reply_text(reply)
        return

    word_count = 0
    for word in words[1:]:
        is_word = any(letter.isalpha() for letter in word)
        if is_word:
            word_count += 1

    reply = f"Найдено {word_count} слова."
    update.message.reply_text(reply)


def next_full_moon(update, context):
    """
    When next full moon after date which user send (or after today if not)
    """
    date_str = " ".join(context.args)

    if not date_str:
        date_from = date.today()
    else:
        date_from = parse(date_str, dayfirst=True)

    full_moon = ephem.next_full_moon(date_from)
    full_moon_string = full_moon.datetime().strftime("%d %B %Y")

    reply = f"Следующее затмение будет {full_moon_string}."

    update.message.reply_text(reply)


def cities(update, context):
    print(context.user_data)
    if not context.args:
        reply = "Введите название города в России"
        update.message.reply_text(reply)
        return

    if "cities_game" not in context.user_data.keys():
        context.user_data["cities_game"] = CitiesSession()

    user_city = "".join(context.args).strip()
    reply = context.user_data["cities_game"].answer(user_city)
    update.message.reply_text(reply)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_where))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("cities", cities))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
