import yaml
import os

from yaml import SafeLoader
from aiogram import Bot, Dispatcher, executor, types
from api import MessageAPI

def get_configuration():
    with open("conf.yml", 'r') as f:
        return yaml.load(f, Loader=SafeLoader) 


config = get_configuration()
token = config.get('bot_token')
shopping_area = config.get('shopping_area')

bot: Bot = Bot(token=token)
dp: Dispatcher = Dispatcher(bot)

message_api = MessageAPI()


@dp.message_handler(commands=["hello", "start"])
async def start(message: types.Message):
    data = {
        'id': message.message_id,
        'text': message.text,
        'unix_time': message.date.isoformat(),
        'is_bot': message.from_user.is_bot,
        'user_id': message.from_user.id
    }
    message_api.create(data)
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
