import logging
from aiogram import Bot, types, Dispatcher, executor
import configparser 
import text as t
from sqlyghter import Sqloghter
import button as bt

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


@dp.message_handler(commands=['go_test'])#тут добаление пользователя в базу данных и начало прохождения теста
async def start(message: types.Message):
    if(db.check_exists_user(message.from_user.id) == 0):
        db.add_user_in_users(message.from_user.id)
        db.add_user_in_cat(message.from_user.id)
        #если юзера нет в базе, то добавляем его и следующая строка вносит изменения а бд
        # db.connection.commit()
        db.commit()
        # и тут начинаем проходить тест. Создаём кнопки и первый вопрос
        text = t.text_for_question_1
        markup = bt.get_markup_reply_test('01', '11', '21', '31', '41', '51')
        await bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode='HTML')
    else:#если пользователь есть в бд уже, то проверяется прошёл ли он тест раньше
        if(db.check_passed_the_test(message.from_user.id) == 0):
            textt = "Видимо раньше вы уже начинали проходить тест, но не закончили начатое."
        elif(db.check_passed_the_test(message.from_user.id) == 1):
            textt = "Раннее вы уже проходили тест!\nПовторное прохождение теста обновит старый результат!"
        markup = bt.get_any_two_buttons("Пройти тест заново", "Не буду проходить", 'good', 'bad')
        await message.answer(textt, reply_markup = markup)

@dp.callback_query_handler(text = 'good')
@dp.callback_query_handler(text = 'bad')
async def begining_over_test(call: types.CallbackQuery):
    answer = call.data
    if answer == 'good':
        db.update_indicate_user(call.from_user.id, 0)
        db.commit()
        text = t.text_for_question_1
        markup = bt.get_markup_reply_test('01', '11', '21', '31', '41', '51')
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')
    elif answer == 'bad':
        text = 'Нет, так нет'
        # и выдать ему старый результат
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, text, parse_mode='HTML')

# Приём ответа на 1 вопрос, задача второго
@dp.callback_query_handler(text = '01')
@dp.callback_query_handler(text = '11')
@dp.callback_query_handler(text = '21')
@dp.callback_query_handler(text = '31')
@dp.callback_query_handler(text = '41')
@dp.callback_query_handler(text = '51')
async def answer_for_extrovert(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '01':
        degry = 0
    elif answer == '11':
        degry = 1
    elif answer == '21':
        degry = 2
    elif answer == '31':
        degry = 3
    elif answer == '41':
        degry = 4
    elif answer == '51':
        degry = 5 
    else: degry = 0
    column_name = 'extrovert'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_2
    markup = bt.get_markup_reply_test('02', '12', '22', '32', '42', '52')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    