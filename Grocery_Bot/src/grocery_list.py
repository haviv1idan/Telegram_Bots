# def write_to_csv(table, parsed_data: list[dict[str, str]]):
#     with open(FILENAME, 'a') as f:
#         writer = csv.DictWriter(f, fieldnames=table.headers)
#         writer.writeheader()
#         writer.writerows(parsed_data)
#
# def read_csv(filename):
#     with open(filename, mode='r') as file:
#         reader = csv.DictReader(file)
#         data = [row for row in reader]
#     return data
"""
This script looking for product and get with the website chp.co.il the best prices in selected area
The script work like this:
 - There is JSON of Products
 - Each Product contain all tables content about his price in different shops

Example:
    {
    Product(
        name: milk,
        id: barcode,
        shops:
        {
            index: {
                    content
                }
        },
        online_shops:
        {
        }
    )
}
"""

import json
import logging

from Grocery_Bot.src.constants import *
from Grocery_Bot.src.classes import *
from selenium import webdriver
from selenium.webdriver.common.by import By


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("grocery_list")


def print_table(table):
    print(("{:<50}" * len(table.headers)).format(*table.headers))
    for row, data in table.body.items():
        print(("{:<50}" * len(table.headers)).format(*data.values()))


def get_products_id_from_file():
    try:
        with open("products.txt", 'r') as file:
            products = file.readlines()
        return products
    except FileNotFoundError as e:
        logger.error(e)
        return None


def write_products_to_file(products):
    with open(PRODUCTS_DETAILS, "w") as file:
        file.write(json.dumps(products))


def get_all_products() -> None:
    """
    Get for each product all stores and prices from website chp.co.il.
    for each product, store the stores and prices in dictionary.
    The dictionary contains the product name and the list of stores and prices.
    :return: None
    """

    # Clear file
    with open(PRODUCTS_DETAILS, 'w') as file:
        file.write("")

    browser = webdriver.Firefox()
    browser.get(WEBSITE)
    web_page = WebPage(browser, WEBSITE)
    web_page.fill_product_filter_field(By.NAME, "shopping_address", SHOPPING_AREA)
    
    if not get_products_id_from_file():
        browser.quit()

    products_ids = get_products_id_from_file()
    products_dict: dict[str, Product] = {}
    
    for product_id in products_ids:

        product = Product(product_id)
        tables_list = web_page.get_all_tables(product_id)

        for table in tables_list:
            if table.attrs.get("style") == "display: inline-block":
                product.name = table.find("h3").contents[0].text

            # filter non results table
            if "results-table" not in table.attrs.get("class", ""):
                continue

            # Table headers
            headers = [th.text for th in table.find("thead").find("tr").find_all("th")]
            logger.info(f"got headers: {headers}")

            # Table Body
            body_content = [tr for tr in table.find("tbody").find_all("tr")
                            if "display_when_narrow" not in tr.attrs.get("class", "")]
            logger.info(f"got body: {body_content}")

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

        products_dict[product.name] = product.__str__()
        logger.info(f"adding {product.name} to products.\nproduct details:\n{product.__str__()}")

    print(f"products: {json.dumps(products_dict)}")

    write_products_to_file(products_dict)

    browser.quit()
