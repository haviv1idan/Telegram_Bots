from Grocery_Bot.main import get_config_file

config_file = get_config_file()

WEBSITE = config_file['website']
SHOPPING_AREA = config_file['shopping_area']
PRODUCTS_FILE = config_file['products_file']
PRODUCTS_DETAILS = config_file['products_details']
BOT_TOKEN = config_file['bot_token']
