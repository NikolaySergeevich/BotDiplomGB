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

@dp.callback_query_handler(text = '02')
@dp.callback_query_handler(text = '12')
@dp.callback_query_handler(text = '22')
@dp.callback_query_handler(text = '32')
@dp.callback_query_handler(text = '42')
@dp.callback_query_handler(text = '52')
async def answer_for_introvert(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '02':
        degry = 0
    elif answer == '12':
        degry = 1
    elif answer == '22':
        degry = 2
    elif answer == '32':
        degry = 3
    elif answer == '42':
        degry = 4
    elif answer == '52':
        degry = 5 
    else: degry = 0
    column_name = 'introvert'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_3
    markup = bt.get_markup_reply_test('03', '13', '23', '33', '43', '53')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 3 вопрос, задача 4 
@dp.callback_query_handler(text = '03')
@dp.callback_query_handler(text = '13')
@dp.callback_query_handler(text = '23')
@dp.callback_query_handler(text = '33')
@dp.callback_query_handler(text = '43')
@dp.callback_query_handler(text = '53')
async def answer_for_ability_to_work_monotonously(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '03':
        degry = 0
    elif answer == '13':
        degry = 1
    elif answer == '23':
        degry = 2
    elif answer == '33':
        degry = 3
    elif answer == '43':
        degry = 4
    elif answer == '53':
        degry = 5 
    else: degry = 0
    column_name = 'ability_to_work_monotonously'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_4
    markup = bt.get_markup_reply_test('04', '14', '24', '34', '44', '54')
    
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 4 вопрос, задача 5 
@dp.callback_query_handler(text = '04')
@dp.callback_query_handler(text = '14')
@dp.callback_query_handler(text = '24')
@dp.callback_query_handler(text = '34')
@dp.callback_query_handler(text = '44')
@dp.callback_query_handler(text = '54')
async def answer_for_mentoring(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '04':
        degry = 0
    elif answer == '14':
        degry = 1
    elif answer == '24':
        degry = 2
    elif answer == '34':
        degry = 3
    elif answer == '44':
        degry = 4
    elif answer == '54':
        degry = 5 
    else: degry = 0
    column_name = 'mentoring'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_5
    markup = bt.get_markup_reply_test('05', '15', '25', '35', '45', '55')
   
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 5 вопрос, задача 6 
@dp.callback_query_handler(text = '05')
@dp.callback_query_handler(text = '15')
@dp.callback_query_handler(text = '25')
@dp.callback_query_handler(text = '35')
@dp.callback_query_handler(text = '45')
@dp.callback_query_handler(text = '55')
async def answer_for_analytical_skills(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '05':
        degry = 0
    elif answer == '15':
        degry = 1
    elif answer == '25':
        degry = 2
    elif answer == '35':
        degry = 3
    elif answer == '45':
        degry = 4
    elif answer == '55':
        degry = 5 
    else: degry = 0
    column_name = 'analytical_skills'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_6
    markup = bt.get_markup_reply_test('06', '16', '26', '36', '46', '56')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 6 вопрос, задача 7 
@dp.callback_query_handler(text = '06')
@dp.callback_query_handler(text = '16')
@dp.callback_query_handler(text = '26')
@dp.callback_query_handler(text = '36')
@dp.callback_query_handler(text = '46')
@dp.callback_query_handler(text = '56')
async def answer_for_empathy(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '06':
        degry = 0
    elif answer == '16':
        degry = 1
    elif answer == '26':
        degry = 2
    elif answer == '36':
        degry = 3
    elif answer == '46':
        degry = 4
    elif answer == '56':
        degry = 5 
    else: degry = 0
    column_name = 'empathy'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_7
    markup = bt.get_markup_reply_test('07', '17', '27', '37', '47', '57')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 7 вопрос, задача 8 
@dp.callback_query_handler(text = '07')
@dp.callback_query_handler(text = '17')
@dp.callback_query_handler(text = '27')
@dp.callback_query_handler(text = '37')
@dp.callback_query_handler(text = '47')
@dp.callback_query_handler(text = '57')
async def answer_for_curiosity(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '07':
        degry = 0
    elif answer == '17':
        degry = 1
    elif answer == '27':
        degry = 2
    elif answer == '37':
        degry = 3
    elif answer == '47':
        degry = 4
    elif answer == '57':
        degry = 5 
    else: degry = 0
    column_name = 'curiosity'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_8
    markup = bt.get_markup_reply_test('08', '18', '28', '38', '48', '58')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 8 вопрос, задача 9 
@dp.callback_query_handler(text = '08')
@dp.callback_query_handler(text = '18')
@dp.callback_query_handler(text = '28')
@dp.callback_query_handler(text = '38')
@dp.callback_query_handler(text = '48')
@dp.callback_query_handler(text = '58')
async def answer_for_oratory(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '08':
        degry = 0
    elif answer == '18':
        degry = 1
    elif answer == '28':
        degry = 2
    elif answer == '38':
        degry = 3
    elif answer == '48':
        degry = 4
    elif answer == '58':
        degry = 5 
    else: degry = 0
    column_name = 'oratory'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_9
    markup = bt.get_markup_reply_test('09', '19', '29', '39', '49', '59')
   
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 9 вопрос, задача 10 
@dp.callback_query_handler(text = '09')
@dp.callback_query_handler(text = '19')
@dp.callback_query_handler(text = '29')
@dp.callback_query_handler(text = '39')
@dp.callback_query_handler(text = '49')
@dp.callback_query_handler(text = '59')
async def answer_for_organizational_skills(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '09':
        degry = 0
    elif answer == '19':
        degry = 1
    elif answer == '29':
        degry = 2
    elif answer == '39':
        degry = 3
    elif answer == '49':
        degry = 4
    elif answer == '59':
        degry = 5 
    else: degry = 0
    column_name = 'organizational_skills'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_10
    markup = bt.get_markup_reply_test('010', '110', '210', '310', '410', '510')
    
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 10 вопрос, задача 11 
@dp.callback_query_handler(text = '010')
@dp.callback_query_handler(text = '110')
@dp.callback_query_handler(text = '210')
@dp.callback_query_handler(text = '310')
@dp.callback_query_handler(text = '410')
@dp.callback_query_handler(text = '510')
async def answer_for_critical_thinking(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '010':
        degry = 0
    elif answer == '110':
        degry = 1
    elif answer == '210':
        degry = 2
    elif answer == '310':
        degry = 3
    elif answer == '410':
        degry = 4
    elif answer == '510':
        degry = 5 
    else: degry = 0
    column_name = 'critical_thinking'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_11
    markup = bt.get_markup_reply_test('011', '111', '211', '311', '411', '511')
    
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 11 вопрос, задача 12 
@dp.callback_query_handler(text = '011')
@dp.callback_query_handler(text = '111')
@dp.callback_query_handler(text = '211')
@dp.callback_query_handler(text = '311')
@dp.callback_query_handler(text = '411')
@dp.callback_query_handler(text = '511')
async def answer_for_multitasking(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '011':
        degry = 0
    elif answer == '111':
        degry = 1
    elif answer == '211':
        degry = 2
    elif answer == '311':
        degry = 3
    elif answer == '411':
        degry = 4
    elif answer == '511':
        degry = 5 
    else: degry = 0
    column_name = 'multitasking'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_12
    markup = bt.get_markup_reply_test('012', '112', '212', '312', '412', '512')
    
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 12 вопрос, задача 13 
@dp.callback_query_handler(text = '012')
@dp.callback_query_handler(text = '112')
@dp.callback_query_handler(text = '212')
@dp.callback_query_handler(text = '312')
@dp.callback_query_handler(text = '412')
@dp.callback_query_handler(text = '512')
async def answer_for_creativity(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '012':
        degry = 0
    elif answer == '112':
        degry = 1
    elif answer == '212':
        degry = 2
    elif answer == '312':
        degry = 3
    elif answer == '412':
        degry = 4
    elif answer == '512':
        degry = 5 
    else: degry = 0
    column_name = 'creativity'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_13
    markup = bt.get_markup_reply_test('013', '113', '213', '313', '413', '513')
   
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 13 вопрос, задача 14 
@dp.callback_query_handler(text = '013')
@dp.callback_query_handler(text = '113')
@dp.callback_query_handler(text = '213')
@dp.callback_query_handler(text = '313')
@dp.callback_query_handler(text = '413')
@dp.callback_query_handler(text = '513')
async def answer_for_stress_resistance(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '013':
        degry = 0
    elif answer == '113':
        degry = 1
    elif answer == '213':
        degry = 2
    elif answer == '313':
        degry = 3
    elif answer == '413':
        degry = 4
    elif answer == '513':
        degry = 5 
    else: degry = 0
    column_name = 'stress_resistance'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_14
    markup = bt.get_markup_reply_test('014', '114', '214', '314', '414', '514')
    
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

# Приём ответа на 14 вопрос, задача 15 
@dp.callback_query_handler(text = '014')
@dp.callback_query_handler(text = '114')
@dp.callback_query_handler(text = '214')
@dp.callback_query_handler(text = '314')
@dp.callback_query_handler(text = '414')
@dp.callback_query_handler(text = '514')
async def answer_for_time_control(call: types.CallbackQuery):
    answer = call.data
    degry = 0
    if answer == '014':
        degry = 0
    elif answer == '114':
        degry = 1
    elif answer == '214':
        degry = 2
    elif answer == '314':
        degry = 3
    elif answer == '414':
        degry = 4
    elif answer == '514':
        degry = 5 
    else: degry = 0
    column_name = 'time_control'
    db.update_degry_whis_dinamic_reqest(call.from_user.id, column_name, degry)
    db.commit()
    # метод, который вносит данные в таблицу теста
    text = t.text_for_question_15
    markup = bt.get_markup_reply_test('015', '115', '215', '315', '415', '515')
   
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode='HTML')

@dp.message_handler(commands=['get_graf_analist'])
async def start(message: types.Message):
    with open(t.get_way_of_img('analist'), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo = photo)

@dp.message_handler(commands=['get_graf_developer'])
async def start(message: types.Message):
    with open(t.get_way_of_img('developer'), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo = photo)

@dp.message_handler(commands=['get_graf_tester']) 
async def start(message: types.Message):
    with open(t.get_way_of_img('tester'), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo = photo)

@dp.message_handler(commands=['get_graf_project'])
async def start(message: types.Message):
    with open(t.get_way_of_img('project'), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo = photo)

@dp.message_handler(commands=['get_graf_prodact'])
async def start(message: types.Message):
    with open(t.get_way_of_img('prodact'), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo = photo)    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    