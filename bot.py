import logging
from aiogram import Bot, types, Dispatcher, executor
import configparser 
import text as t

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'D:/Учёба в GB/Диплом/mylog.log')

config = configparser.ConfigParser()  
config.read("D:/Учёба в GB/Диплом/configs.ini")  

bot = Bot(token = config["Bot"]["token"])
dp = Dispatcher(bot)

@dp.message_handler()
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)

@dp.message_handler(commands=['start'])#тут приветствие
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, t.hello_text.format(name=message.from_user.full_name), parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    