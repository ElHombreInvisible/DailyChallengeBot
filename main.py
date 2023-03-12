
import logging
import os
import requests
from dotenv import load_dotenv
from pprint import pprint

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import Updater, filters, MessageHandler
from dotenv import load_dotenv
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler

FORMAT_FOR_LOGS = ('%(asctime)s, %(levelname)s, %(name)s,'
                   + ' %(funcName)s`, %(message)s')
logging.basicConfig(
        format=FORMAT_FOR_LOGS
    )
logger = logging.getLogger(__name__)
fmt = logging.Formatter(fmt=FORMAT_FOR_LOGS, style='%')
file_logger = logging.FileHandler(filename='main.log',
                                  mode='a', encoding='utf-8')
logger.setLevel('INFO')
file_logger.setFormatter(fmt)
logger.addHandler(file_logger)

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')


builder = Application.builder()
builder.token(token)
application = builder.build()
# application = ApplicationBuilder().token(token).build()
URL = 'https://api.thecatapi.com/v1/images/search'


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id,
#                                    text=f"Howdy, {update.effective_chat.first_name}!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # вложенность не больше 2-х
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
            InlineKeyboardButton("Option 6", callback_data="6"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
        [InlineKeyboardButton("Option 4", callback_data="4")],
        [
         InlineKeyboardButton("Option 5", callback_data="5"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    print(update.callback_query.data)
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE, text_caps='Message is Empty!'):
    if context.args != []:
        print(context.args)  # context.args входящее разбивает сообщение на список, разделитель - пробел
        text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong command!")




if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)
    application.run_polling()
