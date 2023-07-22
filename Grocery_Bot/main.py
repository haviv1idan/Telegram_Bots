import bs4
import logging
import yaml

from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from yaml.loader import SafeLoader
from Grocery_Bot.src.classes import Product
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


SHOP_HEADERS_LENGTH = 6
ONLINE_HEADERS_LENGTH = 5
EMPTY_SALE_VALUE = ' '
HEBREW_SALE_VALUE = 'מבצע'


class SeleniumKeyMissingException(Exception):
    pass


def get_config() -> dict[str, str]:
    """
    get configuration from config file

    :return: configuration
    """
    with open('conf.yml') as f:
        return yaml.load(f, Loader=SafeLoader)


config = get_config()
BOT_TOKEN: str = config['bot_token']
shopping_area: str = config['shopping_area']


# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing bot and dispatcher
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)


def get_driver(website, headless=False) -> webdriver.firefox:
    """
    Get driver to get products details from website

    :param website: the website to get products
    :param headless: boolean if true then run driver in background instead of front
    :return: webdriver.firefox driver
    """
    if headless:
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
    else:
        driver = webdriver.Firefox()
    driver.get(website)
    return driver


def send_filters(driver: webdriver.firefox, elem_type: By, key: str, value: str) -> None:
    """
    Send data to selected element in driver

    :param driver: webdriver.firefox - webdriver driver
    :param elem_type: By - type of page element
    :param key: str - indicator of element
    :param value: str - the value we want to set in element
    :return: None
    """
    element = driver.find_element(elem_type, key)
    element.send_keys(value)
    logger.info("sending %s: %s", key, value)


def filter_table_content(table, product) -> Product | None:
    """
    Got a product table content from the browser.

    :param table: selenium table object
    :param product: str - product id
    :return: updated product object with table content or None
    """

    if table.attrs.get("style") == "display: inline-block":
        product.name = table.find("h3").contents[0].text

    # filter non results table
    if "results-table" not in table.attrs.get("class", ""):
        return

    # Table headers
    t_head = table.find('thead')
    if not t_head:
        raise SeleniumKeyMissingException('Expected to find thead key in table')

    tr = t_head.find('tr')
    if not tr:
        raise SeleniumKeyMissingException('Expected to find tr key in t_head')

    th = tr.find('th')
    if not th:
        raise SeleniumKeyMissingException('Expected to find th key in tr')

    headers: list[str] = [th.text for th in tr if type(th) == bs4.element.Tag]
    logger.info(f"got headers: {headers}")
    if len(headers) == SHOP_HEADERS_LENGTH:
        product.shops.keys = headers
        table_type = 'shops'
    else:
        product.online_shops.keys = headers
        table_type = 'online_shops'

    # Table Body
    t_body = table.find('tbody')
    if not t_body:
        raise SeleniumKeyMissingException('Expected to find tbody key in table')

    tr_list = t_body.find_all('tr')
    if not tr_list:
        raise SeleniumKeyMissingException('Expected to find at least one tr in t_body')

    body_content = [tr for tr in tr_list if "display_when_narrow" not in tr.attrs.get("class", "")]
    logger.info(f"got body: {body_content}")

    for row_index, tr in enumerate(body_content):

        row_content = {}
        td_list = tr.find_all('td')
        if not td_list:
            continue

        for td_index, td in enumerate(td_list):

            if headers[td_index] != HEBREW_SALE_VALUE:
                row_content[headers[td_index]] = td.text
                continue

            try:
                if td.next.get("type") == "button":
                    row_content[headers[td_index]] = td.next.get("data-discount-desc").replace("<BR>", " ")
            except AttributeError:
                row_content[headers[td_index]] = td.text if td.text != EMPTY_SALE_VALUE else ''

        if table_type == 'shops':
            product.shops.values = row_content
        else:
            product.online_shops.values = row_content

    return product


def get_product_details(driver, product_id) -> Product:
    """
    Get product details

    :param driver: webdriver.firefox
    :param product_id: str - product id
    :return: Product object
    """
    product_html: str = driver.page_source
    logger.info("got product_html: %s", product_html)
    soup = BeautifulSoup(product_html, "html.parser")
    result_div = soup.find("div", {"id": "compare_results"})
    tables: list[bs4.element.Tag] = [table for table in result_div.find_all("table")]
    logger.info("got tables: %s", tables)

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


@dp.message_handler(commands=['product'])
async def product_details(message: types.Message):
    # get product id
    product_id: str = message.text.split(' ')[1]
    logger.info("got product_id: %s", product_id)

    # set up driver and send filters
    website = "https://chp.co.il"
    driver = get_driver(website)
    send_filters(driver, By.NAME, "shopping_address", shopping_area)
    send_filters(driver, By.NAME, "product_name_or_barcode", product_id)
    driver.find_element(By.ID, "get_compare_results_button").click()

    try:
        # get product details and parse
        product: Product = get_product_details(driver, product_id)
        driver.quit()
        await message.reply(product.print_product_details())
    except (Exception, ) as e:
        driver.quit()
        logger.error(e)
        await message.reply(f"got exception: {e}")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
