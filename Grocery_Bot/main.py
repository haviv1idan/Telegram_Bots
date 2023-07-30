from aiogram import executor
from Grocery_Bot.conf import CONFIG
from Grocery_Bot.src.bot_messages_handler import *


if __name__ == '__main__':
    executor.start_polling(CONFIG.dispatcher, skip_updates=True)
