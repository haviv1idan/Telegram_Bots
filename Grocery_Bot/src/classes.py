import logging
import os
import json
import time
from typing import Any

import bs4

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.DEBUG)


class Config:

    def __init__(self, config_content: dict[str, str]):
        self.bot_token = config_content['bot_token']
        self.website_url: str = config_content['website_url']
        self.shopping_area = config_content['shopping_area']
        self.products_ids_file_path: str = config_content['products_ids_file_path']
        self.products_details_file_path: str = config_content['products_details_file_path']

    def __str__(self):
        return "config_details: %s" % json.dumps(self.__dict__, indent=4)


class Product:
    """
    This class represent product object
    """
    def __init__(self, product_id):
        self.id: str = product_id
        self.name: str = ""
        self.shops: dict[str, Any] | None = None
        self.online_shops: dict[str, Any] | None = None

    def __str__(self):
        return {"name": self.name, "id": self.id, "shops": self.shops, "online_shops": self.online_shops}

    def _shops_to_string(self, online=False) -> str:
        shops_str = ""
        for i, shop in getattr(self, f"{'online_' if online else ''}shops").items():
            shops_str += f"shop index: {i}\n"
            for key, value in shop.items():
                shops_str += f"\t{key}: {value}\n"
            shops_str += "\n"
        return shops_str

    def print_product_details(self):
        return f"product name: {self.name}\n" \
               f"product id:{self.id}\n" \
               f"shops: \n{self._shops_to_string()}" \
               f"online_shops: \n{self._shops_to_string(online=True)}"


class WebPage:
    """
    This class represent web page object per product
    """

    def __init__(self, url: str):
        # self.options = Options()
        # self.options.add_argument("--headless")
        self.browser = webdriver.Firefox()
        self.url: str = url
        self.browser.get(self.url)

    def fill_product_filter_field(self, field_type: str, field_name: str, value: str):
        # Fill the searching field
        product_indicator = self.browser.find_element(field_type, field_name)
        product_indicator.send_keys("")
        time.sleep(1)
        product_indicator.send_keys(value)
        time.sleep(1)

    def get_all_tables(self, product_id: str) -> list[bs4.element.Tag]:
        """
        find all tables in the given browser
        :return: list of all tables in the given page
        """

        # Fill the searching field
        self.fill_product_filter_field(By.NAME, "product_name_or_barcode", product_id)

        # Click on the search button
        self.browser.find_element(By.ID, "get_compare_results_button").click()
        time.sleep(1)

        table_html = self.browser.page_source
        soup = BeautifulSoup(table_html, "html.parser")
        result_div = soup.find("div", {"id": "compare_results"})
        tables: list[bs4.element.Tag] = [table for table in result_div.find_all("table")]

        return tables


class Products:

    def __init__(self, config: Config):
        self.config: Config = config
        self.products: dict[str, Product] = {}
        self.logger = logging.getLogger("Products_class")

    def get_all_product_ids(self) -> None:
        with open(f"{os.getcwd()}/{self.config.products_ids_file_path}", "r") as f:
            product_ids = f.read().splitlines()

        self.products: dict[str, Product] = {p_id: Product(p_id) for p_id in product_ids}

    def write_products_to_file(self) -> None:
        with open(f"{os.getcwd()}/{self.config.products_details_file_path}", "w") as file:
            json_products = {p_id: v.__str__() for p_id, v in self.products.items()}
            file.write(json.dumps(json_products))

    def get_all_products(self) -> None:
        """
        Get for each product all stores and prices from website chp.co.il.
        for each product, store the stores and prices in dictionary.
        The dictionary contains the product name and the list of stores and prices.
        :return: None
        """

        # Clear file
        products_details_file_full_path = f"{os.getcwd()}/{self.config.products_details_file_path}"
        with open(products_details_file_full_path, 'w') as file:
            file.write("")

        self.get_all_product_ids()

        web_page = WebPage(self.config.website_url)
        web_page.fill_product_filter_field(By.NAME, "shopping_address", self.config.shopping_area)

        if not self.products:
            web_page.browser.quit()

        products_ids = list(self.products.keys())

        for product_id in products_ids:

            tables_list = web_page.get_all_tables(product_id)

            for table in tables_list:
                if table.attrs.get("style") == "display: inline-block":
                    self.products[product_id].name = table.find("h3").contents[0].text

                # filter non results table
                if "results-table" not in table.attrs.get("class", ""):
                    continue

                # Table headers
                headers = [th.text for th in table.find("thead").find("tr").find_all("th")]
                self.logger.info(f"got headers: {headers}")

                # Table Body
                body_content = [tr for tr in table.find("tbody").find_all("tr")
                                if "display_when_narrow" not in tr.attrs.get("class", "")]
                self.logger.info(f"got body: {body_content}")

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

                setattr(self.products[product_id], "{}shops".format("online_" if len(headers) == 5 else ""), table_json)

            self.logger.info(f"adding {self.products[product_id].name} to products.\n"
                             f"product details:\n{self.products[product_id].__str__()}")
        try:
            json_products = {p_id: v.__str__() for p_id, v in self.products.items()}
            print(f"products: {json.dumps(json_products)}")

            self.write_products_to_file()
        except Exception as e:
            print(e)
            pass

        web_page.browser.quit()
