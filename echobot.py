#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler,
                          ConversationHandler, CallbackContext)
from telegram import (Update, Bot, ForceReply, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, KeyboardButton)
from classes import AddressBook, Record, Phone, Birthday
import logging
import pyrebase
import urllib
import pickle


firebaseConfig = {
    "apiKey": "AIzaSyDyPGUebWDC7ojqNgjsbnyRTzpq2Odz-Ig",
    "authDomain": "telegrambot-assistants.firebaseapp.com",
    "databaseURL": "https://telegrambot-assistants-default-rtdb.firebaseio.com",
    "projectId": "telegrambot-assistants",
    "storageBucket": "telegrambot-assistants.appspot.com",
    "messagingSenderId": "690275854622",
    "appId": "1:690275854622:web:0ee345449835f4b4b6c10f",
    "measurementId": "G-4MNZJLFN1L"
}
firebase = pyrebase.initialize_app(firebaseConfig)


# db = firebase.database()
# auth = firebase.auth()
storage = firebase.storage()


# FBConn = firebase.FirebaseApplication(
#    'https://telegrambot-assistants-default-rtdb.firebaseio.com', None)


token = "1753379890:AAGP2o4U-DJjX7X5OenBcswPVAoo3ckK56U"
"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

keyboard_start = [
    [InlineKeyboardButton("Добавить запись", callback_data="add_record")],
    [InlineKeyboardButton("Изменить запись", callback_data="change_record")],
    [InlineKeyboardButton("Удалить запись", callback_data="delete_record")],
    [InlineKeyboardButton("Поиск", callback_data="looking_for")],
    [InlineKeyboardButton("Показать все", callback_data="show_all")],
]

keyboard_change_record = [
    [InlineKeyboardButton("Изменить имя", callback_data="change_name")],
    [InlineKeyboardButton("Изменить телефон", callback_data="change_phone")],
    [InlineKeyboardButton("Добавить телефон", callback_data="add_phone")],
    [InlineKeyboardButton("Изменить д/р",  callback_data="change_bd")],
    [InlineKeyboardButton("Изменить адрес", callback_data="change_address")],
    [InlineKeyboardButton("Изменить email", callback_data="change_email")],
    [InlineKeyboardButton("Добавить email", callback_data="add_email")],
    [InlineKeyboardButton("Добавить заметку", callback_data="add_note")],
]


def deserialize_users(url):
    """using the path "path" reads the file with contacts"""
    '''
    with open(filename, 'a') as f:
        f.write(x+'\n')
    storage.child(cloudfilename).put(filename)
    storage.child(cloudfilename).download('', filename)
    with open(filename, 'r') as f:
        x = f.read()
    # print(result)
    
    '''

    try:
        f = urllib.request.urlopen(url).read()
        addressbook = pickle.loads(f)
    except:
        addressbook = ''
    return addressbook


def serialize_users(addressbook, path):
    """saves a file with contacts on the path (object pathlib.Path) to disk"""
    f = pickle.dumps(addressbook)
    print(f)
    storage.child(path).put(f)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # user = update.effective_user
    # update.message.reply_markdown_v2(
    #    fr'Hi {user.mention_markdown_v2()}\!',
    #    reply_markup=ForceReply(selective=True),
    # )
    if update.message is None:
        event = update.callback_query.message
    else:
        event = update.message

    reply_start = InlineKeyboardMarkup(keyboard_start)

    message_start = 'Добро пожаловать в систему личного помощника'
    # event.reply_text(
    #    content1, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
    # если нужно удалить нижнюю клавиатуру reply_markup=ReplyKeyboardRemove()
    # event.reply_photo(url_photo)
    event.reply_text(message_start, reply_markup=reply_start)


def add_record(update: Update, context: CallbackContext) -> None:
    pass


def change_record(update: Update, context: CallbackContext) -> None:
    message = 'Выберите пункт меню'
    reply = InlineKeyboardMarkup(keyboard_change_record)
    event = update.message
    event.reply_text(message, reply_markup=reply)


def delete_record(update: Update, context: CallbackContext) -> None:
    pass


def looking_for(update: Update, context: CallbackContext) -> None:
    pass


def show_all(update: Update, context: CallbackContext) -> None:
    pass


def change_name(update: Update, context: CallbackContext) -> None:
    pass


def change_phone(update: Update, context: CallbackContext) -> None:
    pass


def add_phone(update: Update, context: CallbackContext) -> None:
    pass


def change_bd(update: Update, context: CallbackContext) -> None:
    pass


def change_address(update: Update, context: CallbackContext) -> None:
    pass


def change_email(update: Update, context: CallbackContext) -> None:
    pass


def add_email(update: Update, context: CallbackContext) -> None:
    pass


def add_note(update: Update, context: CallbackContext) -> None:
    pass


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    x = update.message.text

    # Storage
    # print(update)
    # print(type(update.username))
    # print(update.message.chat.username)
    username = update.message.chat.username
    id_user = update.message.chat.id

    filename = f"contacts_{id_user}.txt"
    cloudfilename = f"users/{filename}"
    url = storage.child(cloudfilename).get_url(None)
    addressbook = deserialize_users(url) + x
    print(url, addressbook)
    serialize_users(addressbook, cloudfilename)
    update.message.reply_text(addressbook)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(CallbackQueryHandler(add_record, pattern="add_record"))
    dp.add_handler(CallbackQueryHandler(
        change_record, pattern="change_record"))
    dp.add_handler(CallbackQueryHandler(
        delete_record, pattern="delete_record"))
    dp.add_handler(CallbackQueryHandler(looking_for, pattern="looking_for"))
    dp.add_handler(CallbackQueryHandler(show_all, pattern="show_all"))

    dp.add_handler(CallbackQueryHandler(change_name, pattern="change_name"))
    dp.add_handler(CallbackQueryHandler(change_phone, pattern="change_phone"))
    dp.add_handler(CallbackQueryHandler(add_phone, pattern="add_phone"))
    dp.add_handler(CallbackQueryHandler(change_bd, pattern="change_bd"))
    dp.add_handler(CallbackQueryHandler(
        change_address, pattern="change_address"))
    dp.add_handler(CallbackQueryHandler(change_email, pattern="change_email"))
    dp.add_handler(CallbackQueryHandler(add_email, pattern="add_email"))
    dp.add_handler(CallbackQueryHandler(add_note, pattern="add_note"))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
