import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("7504616814:AAE-toFkzsXufqMIxa-YLuzJhD9P7KfmTSQ")


def get_db_connection():
    conn = sqlite3.connect('referrals.db')
    conn.row_factory = sqlite3.Row
    return conn


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🏦 Получить реферальную ссылку"),
        types.KeyboardButton("ℹ️ Информация")
    )
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для получения реферальных ссылок банков. Выбери действие:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "🏦 Получить реферальную ссылку")
def show_referrals(message):
    conn = get_db_connection()
    referrals = conn.execute('SELECT name, callback FROM referrals').fetchall()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    for ref in referrals:
        markup.add(types.InlineKeyboardButton(ref['name'], callback_data=ref['callback']))

    bot.send_message(message.chat.id, "Выберите карту:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def send_referral(call):
    conn = get_db_connection()
    ref = conn.execute('SELECT content FROM referrals WHERE callback = ?', (call.data,)).fetchone()
    conn.close()

    if ref:
        bot.send_message(call.message.chat.id, ref['content'], parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, "Рефералка не найдена")
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda m: m.text == "ℹ️ Информация")
def info(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Информация о боте:\n\n"
        "Этот бот предоставляет реферальные ссылки для оформления карт.\n"
        "По вопросам обращайтесь к @support",
        parse_mode='HTML'
    )


if __name__ == "__main__":
    bot.polling(none_stop=True)