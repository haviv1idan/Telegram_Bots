import json

from Grocery_Bot.main import TELEBOT, products

bot = TELEBOT


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, I'm bot. Type /help to see the list of commands.")


@bot.message_handler(commands=["products"])
def send_products(message):
    bot.send_message(message.chat.id, message.text)
    json_products = {p_id: v.__str__() for p_id, v in products.products.items()}
    bot.send_message(message.chat.id, json.dumps(json_products))


@bot.message_handler(func=lambda msg: True)
def send_any(message):
    bot.send_message(message.chat.id, message.text)
