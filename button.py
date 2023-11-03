from aiogram import types

def get_markup_reply_test(callback_data1, callback_data2, callback_data3, callback_data4, callback_data5, callback_data6):
    markup = types.InlineKeyboardMarkup(row_width=6)
    item1 = types.InlineKeyboardButton("0", callback_data=callback_data1)
    item2 = types.InlineKeyboardButton("1", callback_data=callback_data2)
    item3 = types.InlineKeyboardButton("2", callback_data=callback_data3)
    item4 = types.InlineKeyboardButton("3", callback_data=callback_data4)
    item5 = types.InlineKeyboardButton("4", callback_data=callback_data5)
    item6 = types.InlineKeyboardButton("5", callback_data=callback_data6)
    markup.add(item1, item2, item3, item4, item5, item6)
    return markup
def get_any_two_buttons(button_1, button_2, callback_data1, callback_data2):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(button_1, callback_data=callback_data1)
    item2= types.InlineKeyboardButton(button_2, callback_data=callback_data2)
    markup.add(item1, item2)
    return markup