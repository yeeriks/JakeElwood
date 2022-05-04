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

users = {}


class User:
    def __init__(self, name):
        self.spike = 0
        self.name = name

    def get_name(self):
        return self.name

    def get_spike(self):
        return self.spike

    def add_spike(self, value):
        self.spike += value

    def clear_spike(self):
        self.spike = 0


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Start by using \'/set_name <name>\' command.\n"
                                  "You can view available commands with /help")


def help_msg(update: Update, context: CallbackContext):
    help_message = "Commands:\n" \
                   "/start - initiates the bot\n" \
                   "/help - bot sends this command list\n" \
                   "/set_name <name> - tells the bot your name\n" \
                   "/add_spike <amount> - adds the value to the spike\n" \
                   "/get_spike - tells the current spike value\n" \
                   "/clear_spike - sets the current spike as 0\n" \
                   "/get_id - tells the user their id"

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=help_message)


def set_name(update: Update, context: CallbackContext):
    try:
        name = context.args[0]
        user_id = update.effective_chat.id
        if name in users:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Name already taken")
            return

        user = User(name)
        users[user_id] = user

        message = "Name set as " + str(name)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message)

    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Usage: /set_name <name>")


def add_spike(update: Update, context: CallbackContext):
    try:
        amount = float(context.args[0])
        amount100 = int(amount*100)

        user = users[update.effective_chat.id]

        user.add_spike(amount100)

        message = str(float(amount100)/100) + " has been added to the spike."
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message)

    except (IndexError, ValueError):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Usage: /add_spike <amount>\n"
                                      "amount must be either an integer or a decimal\n"
                                      "value separated with a decimal point \'.\'")


def get_spike(update: Update, context: CallbackContext):
    userid = update.effective_chat.id
    spike = users[userid].get_spike()
    message = "User " + str(users[userid].get_name()) + " has " + str(float(spike)/100) + " in their spike"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message)


def clear_spike(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user = users[user_id]
    user.clear_spike()
    message = "Spike has been cleared for " + user.get_name()
    context.bot.send_message(chat_id=user_id, text=message)


def get_id(update: Update, context: CallbackContext):
    userid = update.effective_chat.id
    context.bot.send_message(chat_id=userid, text=str(userid))


def main():

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help_msg)
    dispatcher.add_handler(help_handler)

    set_name_handler = CommandHandler('set_name', set_name)
    dispatcher.add_handler(set_name_handler)

    add_spike_handler = CommandHandler('add_spike', add_spike)
    dispatcher.add_handler(add_spike_handler)

    get_spike_handler = CommandHandler('get_spike', get_spike)
    dispatcher.add_handler(get_spike_handler)

    clear_spike_handler = CommandHandler('clear_spike', clear_spike)
    dispatcher.add_handler(clear_spike_handler)

    get_id_handler = CommandHandler('get_id', get_id)
    dispatcher.add_handler(get_id_handler)
    
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
