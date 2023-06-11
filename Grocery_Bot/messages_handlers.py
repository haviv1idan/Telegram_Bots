import telebot

BOT_TOKEN = "6233364747:AAHPZ7PLineWKJcp4v0xx1dEpvvNyzlnqFc"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, I'm bot. Type /help to see the list of commands.")


@bot.message_handler(func=lambda msg: True)
def send_welcome(message):
    bot.send_message(message, message.text)


@bot.message_handler(commands=["get product"])
def send_product_details(message):
    pass
