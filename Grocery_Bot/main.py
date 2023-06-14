import json
from Grocery_Bot.src import messages_handlers

from src.grocery_list import get_all_products


def get_config_file() -> json:
    """
    read bot token from config file
    :return: bot token
    """
    with open('additional_files/config.json', 'r') as f:
        config = json.load(f)
    return config


if __name__ == '__main__':
    get_all_products()
    messages_handlers.bot.infinity_polling()
