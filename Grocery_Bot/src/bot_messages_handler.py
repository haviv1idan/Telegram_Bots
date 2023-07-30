from time import sleep
from aiogram import types
from logging import getLogger
from Grocery_Bot.conf import BOT, DISPATCHER
from Grocery_Bot.src.classes import WebPage
from selenium.webdriver.common.by import By

bot, dp = BOT, DISPATCHER

logger = getLogger(__name__)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logger.info("Got message %s", message)
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['product'])
async def product_details(message: types.Message):
    product_id = message.text.split(' ')[-1]
    logger.info(f"Got product: {product_id}")
    web_page = WebPage(product_id, headers=True)
    web_page.setup_filters()
    try:
        web_page.collect_product_data()
    except Exception as e:
        web_page.driver.quit()
    web_page.driver.quit()
    await message.reply(web_page.product)
