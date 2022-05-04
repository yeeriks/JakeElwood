from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

""" 
JakeElwood.credentials.py contains three attributes:
    bot_token : the token given by BotFather
    bot_user_name : username of this bot
    URL : url for this bot at online hosting service
"""
from JakeElwood.credentials import bot_token


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello, I'm a bot!")


def main():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()