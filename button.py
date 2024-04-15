from aiogram import types
def get_markup_reply_test(callback_data1, callback_data2, callback_data3, callback_data4, callback_data5, callback_data6):
    """Метод принимает шесть аргументов, которые будут являтся возвращаемыми данными при нажатии на кнопки
    Args:
        callback_data1 (_type_): _description_
        callback_data2 (_type_): _description_
        callback_data3 (_type_): _description_
        callback_data4 (_type_): _description_
        callback_data5 (_type_): _description_
        callback_data6 (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """Метод принимает значение для задачи двух кнопок и значения, которые кнопки будут возвращать.
    Args:
        button_1 (_type_): _description_
        button_2 (_type_): _description_
        callback_data1 (_type_): _description_
        callback_data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(button_1, callback_data=callback_data1)
    item2= types.InlineKeyboardButton(button_2, callback_data=callback_data2)
    markup.add(item1, item2)
    return markup