#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

from my_token import token, chat_id
sMyToken = token
import sqlite3
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters




def create_conection(datafile):
    conn = None
    try:
       conn = sqlite3.connect(datafile)
       return conn
    except sqlite3.DatabaseError as e:
        print(e)
        return conn

def exec_sql(conn, sSql):
    try:
        c = conn.cursor()
        c.execute(sSql)
    except sqlite3.DatabaseError as e:
        print(e)

conn = create_conection("timetable.db")

lSql = []
lSql.append(""" CREATE TABLE IF NOT EXISTS timetable (id integer PRIMARY KEY,
                                                      class_id integer not null,  
                                                      lesson_subject_id integer not NULL,
                                                      lesson_index integer not NULL,
                                                      lesson_day_id integer not NULL
                                                      ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS subjects (subject_id integer PRIMARY KEY,
                                                     subject_name text not NULL,
                                                     subject_tutor text  not NULL
                                                 ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS dow (day_id integer PRIMARY KEY,
                                                day_name text not NULL
                                                ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS classes (class_id integer PRIMARY KEY,
                                                    class_grade integer not NULL,
                                                    class_letter text not null
                                                    ); """)

for sSql in lSql:
    exec_sql(conn, sSql)

lSubList = ["алгебра"
,"химия"
,"физика"
,"география"
,"физкультура"
,"английский"
,"информатика"
,"история"
,"русский"
,"литература"
,"геометрия"
,"биология"
,"обж"]

lDayOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


for i, sName in enumerate(lSubList):
    #exec_sql(conn, f'insert into subjects (subject_id, subject_name, subject_tutor) values ({i}, {sName}, "Noname")')
    sSql = f"insert into subjects (subject_id, subject_name, subject_tutor) values ('{i}', '{sName}', '{sName}')"
    exec_sql(conn, sSql)





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
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='telebot.log')

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello. To get commands send /help!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/timetable <N><L> where N - class grade L - class letter')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def caps(update, context):
    '''Cocky'''
    update.message.reply_text(' '.join(context.args))

def timetable(update, context):
    '''Random film'''
    sHeader = f'Timetable for {context.args} is:'
    update.message.reply_text(sHeader) #' '.join(context.args))
    print(context.args)

def author(update, context):
    sMessage = 'Jury A Kondratyev'
    update.message.reply_text(sMessage)

#def sc(update, context):
#    counter = symbol_count(update.message.text[4:])
#    response = '\n'.join(f'"{symbol}": {count}' for symbol, count in counter.items())
#    update.message.reply_text(response)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = sMyToken
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("author", author))

    # my own handlers
    #dp.add_handler(CommandHandler('caps', caps, pass_args=True))
    dp.add_handler(CommandHandler('timetable', timetable, pass_args=True))
    #dp.add_handler(CommandHandler('sc', sc))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
