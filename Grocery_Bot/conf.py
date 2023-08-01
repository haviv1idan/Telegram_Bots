import yaml
import json
import logging

from typing import Any
from aiogram import Bot, Dispatcher
from yaml import SafeLoader
from logging import getLogger

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)


def get_config() -> dict[str, str]:
    """
    get configuration from config file

    :return: configuration dictionary
    """
    with open('conf.yml') as f:
        config = yaml.load(f, Loader=SafeLoader)
        logger.info("Config: \n%s" % str(config))
        return config


def get_translation() -> dict[str, str]:
    """
    get translations

    :return: dictionary of translations
    """
    with open("src/translation.json", 'r') as f:
        translation = json.load(f)
        logger.info("Translation: \n%s" % str(translation))
        return translation


def get_all_products_from_file():
    """
    get all products from products.txt

    :return: list of products barcodes
    """
    with open("additional_files/products.txt", 'r') as f:
        barcodes = f.read().split('\n')
        logger.info("barcodes: \n%s" % barcodes)
        return barcodes


class Config:

    def __init__(self):
        self.config_file: dict[str, Any] = get_config()
        self.shopping_area = self.config_file.get('shopping_area')
        self.bot: Bot = Bot(token=self.config_file.get('bot_token'))
        self.dispatcher: Dispatcher = Dispatcher(self.bot)
        self.translation: dict[str, str] = get_translation()
        self.barcodes: list[str] = get_all_products_from_file()

    def update_barcodes(self, barcode):
        self.barcodes.append(barcode)
        with open("additional_files/products.txt", 'w') as f:
            f.write('\n'.join(self.barcodes))


CONFIG = Config()
BOT = CONFIG.bot
DISPATCHER = CONFIG.dispatcher
