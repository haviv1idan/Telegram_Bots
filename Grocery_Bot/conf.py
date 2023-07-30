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


class Config:

    def __init__(self):
        self.config_file: dict[str, Any] = get_config()
        self.shopping_area = self.config_file.get('shopping_area')
        self.bot: Bot = Bot(token=self.config_file.get('bot_token'))
        self.dispatcher: Dispatcher = Dispatcher(self.bot)
        self.translation = get_translation()


CONFIG = Config()
BOT = CONFIG.bot
DISPATCHER = CONFIG.dispatcher
