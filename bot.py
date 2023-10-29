import logging
from aiogram import Bot, types, Dispatcher, executor
import configparser 
import text as t
from sqlyghter import Sqloghter

db = Sqloghter()

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'D:/Учёба в GB/Диплом/mylog.log')

config = configparser.ConfigParser()  
config.read("D:/Учёба в GB/Диплом/configs.ini")  

bot = Bot(token = config["Bot"]["token"])
dp = Dispatcher(bot)

# @dp.message_handler()
# async def start(message: types.Message):
#     await bot.send_message(message.from_user.id, message.text)

@dp.message_handler(commands=['start'])#тут приветствие
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, t.hello_text.format(name=message.from_user.full_name), parse_mode='HTML')


@dp.message_handler(commands=['communicate'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
    item2 = types.InlineKeyboardButton('Нe очень', callback_data='bad')
    markup.add(item1, item2)
    await bot.send_message(message.from_user.id, "Привет, как твои дела?", reply_markup = markup)

@dp.callback_query_handler(text = 'good')
@dp.callback_query_handler(text = 'bad')
async def reply(call: types.CallbackQuery):
    answer = call.data
    if answer == 'good':
        text = "Я рад, что у тебя всё хорошо"
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, text)
    elif answer == 'bad':
        text = 'Хмм, расскажи свои проблемы'
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, text)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    