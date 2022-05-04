from telegram.ext import Updater
from JakeElwood.credentials import bot_token
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello, I'm a bot!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()