import messages_handlers

from src.grocery_list import get_all_products


if __name__ == '__main__':
    get_all_products()
    messages_handlers.bot.infinity_polling()
