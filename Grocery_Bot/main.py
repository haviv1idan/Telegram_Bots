import bs4
import logging

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from Grocery_Bot.src.classes import Product

BOT_TOKEN: str = "6233364747:AAHPZ7PLineWKJcp4v0xx1dEpvvNyzlnqFc"

# Configuring logging
logging.basicConfig(level=logging.INFO)

# Initializing bot and dispatcher
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)
shopping_area = "כביש חולון בת ים, ראשון לציון"


def get_driver():
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://chp.co.il")
    return driver


def send_filters(driver, elem_type, key, value):
    element = driver.find_element(elem_type, key)
    element.send_keys(value)
    logging.info("sending %s: %s", key, value)


def filter_table_content(table, product) -> Product | None:

    if table.attrs.get("style") == "display: inline-block":
        product.name = table.find("h3").contents[0].text

    # filter non results table
    if "results-table" not in table.attrs.get("class", ""):
        return

    # Table headers
    headers = [th.text for th in table.find("thead").find("tr").find_all("th")]
    logging.info(f"got headers: {headers}")

    # Table Body
    body_content = [tr for tr in table.find("tbody").find_all("tr")
                    if "display_when_narrow" not in tr.attrs.get("class", "")]
    logging.info(f"got body: {body_content}")

    table_json = {}
    for row_index, tr in enumerate(body_content):
        row_content = {}
        for td_index, td in enumerate(tr.find_all("td")):

            if headers[td_index] != "מבצע":
                row_content[headers[td_index]] = td.text
                continue

            try:
                if td.next.get("type") == "button":
                    row_content[headers[td_index]] = td.next["data-discount-desc"]
            except AttributeError:
                row_content[headers[td_index]] = td.text

        table_json[row_index] = row_content

    setattr(product, "{}shops".format("online_" if len(headers) == 5 else ""), table_json)
    return product


def get_product_details(driver, product_id) -> Product:
    product_html = driver.page_source
    logging.info("got product_html: %s", product_html)
    soup = BeautifulSoup(product_html, "html.parser")
    result_div = soup.find("div", {"id": "compare_results"})
    tables: list[bs4.element.Tag] = [table for table in result_div.find_all("table")]
    logging.info("got tables: %s", tables)

    product = Product(product_id)
    for table in tables:
        filter_table_content(table, product)

    return product


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['get_product_details'])
async def product_details(message: types.Message):
    # get product id
    product_id: str = message.text.split(' ')[1]
    logging.info("got product_id: %s", product_id)

    # set up driver and send filters
    driver = get_driver()
    send_filters(driver, By.NAME, "shopping_address", shopping_area)
    send_filters(driver, By.NAME, "product_name_or_barcode", product_id)
    driver.find_element(By.ID, "get_compare_results_button").click()

    # get product details and parse
    product: Product = get_product_details(driver, product_id)
    # await message.reply(product.__str__())
    await message.reply(product.print_product_details())


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
