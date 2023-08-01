import threading

from aiogram import types
from logging import getLogger
from Grocery_Bot.conf import BOT, DISPATCHER, CONFIG
from Grocery_Bot.src.classes import WebPage, Product

bot, dp = BOT, DISPATCHER

logger = getLogger(__name__)


def get_product_data(product_id) -> Product:
    web_page = WebPage(product_id, headers=True)
    web_page.setup_filters()
    try:
        web_page.collect_product_data()
        web_page.driver.quit()
    except Exception as e:
        web_page.driver.quit()
    web_page.product.insert_data_to_db()
    return web_page.product


def run_get_product_data_as_thread(product_id_list):
    threads = []
    results = {}

    def thread_func(barcode):
        result = get_product_data(barcode)
        results[barcode] = result

    for product_id in product_id_list:
        thread = threading.Thread(target=thread_func, args=(product_id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results


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
    product = get_product_data(product_id)
    await message.reply(product.__str__())
    if product not in CONFIG.barcodes:
        CONFIG.update_barcodes(product_id)


@dp.message_handler(commands=['all_products'])
async def product_details(message: types.Message):
    threads_results = run_get_product_data_as_thread(CONFIG.barcodes)

    for product_id in CONFIG.barcodes:
        if threads_results.get(product_id):
            await message.reply(threads_results[product_id].__str__())
