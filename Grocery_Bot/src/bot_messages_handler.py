import json
import threading

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from logging import getLogger
from Grocery_Bot.conf import BOT, DISPATCHER, CONFIG
from Grocery_Bot.src.classes import WebPage, Product

bot, dp = BOT, DISPATCHER

logger = getLogger(__name__)


def get_product_name_by_barcode(product_id):
    with open('additional_files/products_details.json', 'r') as f:
        content = json.load(f)
    product_name = content[product_id]['name']
    return product_name


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

    with open('additional_files/products_details.json', 'w') as f:
        results_dicts = {barcode: product.__dict__() for barcode, product in results.items()}
        f.write(json.dumps(results_dicts))

    return results


def generate_inline_keyboard():
    btn_list = []
    for product_id in CONFIG.barcodes:
        product_name = get_product_name_by_barcode(product_id).replace(',', '\n')
        # btn = InlineKeyboardButton(product_name, callback_data=product_name)
        btn = KeyboardButton(product_name, callback_data=product_name)
        btn_list.append([btn])

    # Create individual buttons
    button1 = InlineKeyboardButton("Button 1", callback_data="button1")
    button2 = InlineKeyboardButton("Button 2", callback_data="button2")
    button3 = InlineKeyboardButton("Button 3", callback_data="button3")

    # Create a list of button rows
    button_list = [
        [button1, button2],
        [button3]
    ]

    # Create the keyboard
    # reply_markup = InlineKeyboardMarkup(inline_keyboard=button_list)
    # reply_markup = InlineKeyboardMarkup(inline_keyboard=btn_list)
    reply_markup = ReplyKeyboardMarkup(keyboard=btn_list, resize_keyboard=True)

    return reply_markup


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logger.info("Got message %s", message)
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['inline'])
async def send_inline(message: types.Message):
    # Generate the inline keyboard
    reply_markup = generate_inline_keyboard()

    # Send the message with the inline keyboard
    await message.reply("Choose an option: ", reply_markup=reply_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('button'))
async def process_callback_button(callback_query: types.CallbackQuery):
    # Get the callback_data (button identifier)
    button_clicked = callback_query.data

    # Send a response with the corresponding product_id
    await callback_query.answer(f"You clicked button with product_id: {button_clicked}")


@dp.message_handler(commands=['product'])
async def product_details(message: types.Message):
    product_id = message.text.split(' ')[-1]
    if product_id == '/product':
        await message.reply("No product entered")
    else:
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


@dp.message_handler(commands=['product_name'])
async def product_details(message: types.Message):
    product_id = message.text.split(' ')[-1]
    product_name = get_product_name_by_barcode(product_id)
    await message.reply(product_name)
