import logging

from bs4.element import Tag
from bs4 import BeautifulSoup
from Grocery_Bot.conf import CONFIG
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


SHOP_HEADERS_LENGTH = 6
ONLINE_SHOP_HEADERS_LENGTH = 5


class WebPageTable:

    def __init__(self, is_online=False):
        self.is_online = is_online
        self.headers: list[str] = []
        self.values: list[dict[str, str]] = []

    def __str__(self):
        shops_str = ""
        for i, shop in enumerate(self.values):
            shops_str += f"shop index: {i}\n"
            for key, value in shop.items():
                shops_str += f"\t{key}: {value}\n"
            shops_str += "\n"
        return shops_str


class Product:

    def __init__(self, barcode, name=''):
        self.barcode: str = barcode
        self.name: str = name
        self.shops: WebPageTable = WebPageTable()
        self.online_shops: WebPageTable = WebPageTable(is_online=True)

    def _add_shop(self, data: dict[str, str]):
        pass

    def _add_online_shop(self, data: dict[str, str]):
        pass

    def __str__(self):
        return f"barcode: {self.barcode}\n" \
               f"name: {self.name}\n" \
               f"shops: {self.shops}\n" \
               f"online_shops: {self.online_shops}\n"


class WebPage:

    def __init__(self, product_id: str, headers: bool = False):
        self.logger = logging.getLogger(__name__)
        self._options = Options()
        if headers:
            self._options.add_argument('--headers')
        self.driver = Firefox(options=self._options)
        self.url = 'https://chp.co.il'
        self.driver.get(self.url)
        self.product = Product(product_id)

    def setup_filters(self):
        """
        Setup filters for product details

        :return: None
        """
        self._send_filters(By.NAME, "shopping_address", CONFIG.shopping_area)
        self._send_filters(By.NAME, "product_name_or_barcode", self.product.barcode)
        self.driver.find_element(By.ID, "get_compare_results_button").click()

    def _send_filters(self, elem_type: By, key: str, value: str) -> None:
        """
        Send data to selected element in driver

        :param elem_type: By - type of page element
        :param key: str - indicator of element
        :param value: str - the value we want to set in element
        :return: None
        """
        element = self.driver.find_element(elem_type, key)
        element.send_keys(value)
        self.logger.info("sending %s: %s", key, value)

    def _get_tables_from_web_page(self) -> list[Tag]:
        """
        Get all tables from web page

        :return: list[Tag] - list of web page tables
        """
        product_html: str = self.driver.page_source
        self.logger.info("got product_html: %s", product_html)
        soup = BeautifulSoup(product_html, "html.parser")
        result_div = soup.find("div", {"id": "compare_results"})
        tables: list[Tag] = [table for table in result_div.find_all("table")]
        self.logger.info("got tables: %s", tables)
        return tables

    def _get_table_headers(self, table: Tag) -> list[str]:
        """
        Get table and extract headers from table.
        The function extracts the headers, store them in product and return them

        :param table: Tag - table to extract headers
        :return: table type
        """
        # Table headers
        t_head = table.find('thead')
        if not t_head:
            raise KeyError('Expected to find thead key in table: %s' % table)

        tr = t_head.find('tr')
        if not tr:
            raise KeyError('Expected to find tr key in t_head: %s' % t_head)

        th = tr.find('th')
        if not th:
            raise KeyError('Expected to find th key in tr: %s' % tr)

        headers: list[str] = [th.text for th in tr if type(th) == Tag]
        self.logger.info('Got headers: %s' % headers)
        if len(headers) == SHOP_HEADERS_LENGTH:
            self.product.shops.headers = headers
        else:
            self.product.online_shops.headers = headers
        return headers

    def _filter_body_content(self, table: Tag, table_type: str) -> None:
        """
        Got body content of table and extract the relevant data of the product

        :param table: Tag - table to product content
        :param table_type: str - online_shops / shops
        :return: None
        """
        # Table Body
        t_body = table.find('tbody')
        if not t_body:
            raise KeyError('Expected to find tbody key in table')

        tr_list = t_body.find_all('tr')
        if not tr_list:
            raise KeyError('Expected to find at least one tr in t_body: %s' % t_body)

        body_content = [tr for tr in tr_list if 'display_when_narrow' not in tr.attrs.get('class', '')]
        self.logger.info(f"got body: {body_content}")

        headers = getattr(self.product, table_type).headers

        for row_index, tr in enumerate(body_content):

            row_content = {}
            td_list = tr.find_all('td')
            if not td_list:
                continue

            for td_index, td in enumerate(td_list):

                if headers[td_index] != CONFIG.translation.get('sale'):
                    row_content[headers[td_index]] = td.text
                    continue

                try:
                    if td.next.get("type") == "button":
                        row_content[headers[td_index]] = td.next.get("data-discount-desc").replace("<BR>", " ")
                except AttributeError:
                    row_content[headers[td_index]] = td.text if td.string != '\xa0' else ''

            if table_type == 'shops':
                self.product.shops.values.append(row_content)
            else:
                self.product.online_shops.values.append(row_content)

    def _filter_table_content(self, table: Tag) -> None:
        """
        filter table content and update product

        :param table: Tag - shop/online_shop table
        :return: None - update product object
        """
        if table.attrs.get("style") == "display: inline-block":
            self.product.name = table.find("h3").contents[0].text

            # filter non results table
        if "results-table" not in table.attrs.get("class", ""):
            return

        table_headers = self._get_table_headers(table)
        table_type = 'shops' if len(table_headers) == SHOP_HEADERS_LENGTH else 'online_shops'
        self._filter_body_content(table, table_type)

    def collect_product_data(self):
        """
        Collect product data from driver

        :return: Product object
        """
        tables = self._get_tables_from_web_page()

        for table in tables:
            self._filter_table_content(table)
